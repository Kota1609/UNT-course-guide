import fs from 'fs/promises';
import path from 'path';
import { config } from 'dotenv';
import OpenAI from 'openai';
import { Pinecone } from '@pinecone-database/pinecone';
import { encoding_for_model } from '@dqbd/tiktoken';
import csv from 'csvtojson';

// Load env vars
config({ path: '.env.local' });

const CSV_PATH = path.resolve(process.cwd(), 'final_merged_courses_data.csv');
const INDEX_NAME = process.env.PINECONE_INDEX_NAME!;
const EMBEDDING_MODEL = 'text-embedding-ada-002';
const MAX_TOKENS = 8191;

// Clients
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });
const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });

// Token-based chunking
async function chunkTextTokenStrict(text: string, maxTokens = MAX_TOKENS): Promise<string[]> {
  const enc = await encoding_for_model(EMBEDDING_MODEL);
  const tokens = enc.encode(text);
  const chunks: string[] = [];

  for (let i = 0; i < tokens.length; i += maxTokens) {
    const chunkTokens = tokens.slice(i, i + maxTokens);
    const decoded = Buffer.from(enc.decode(chunkTokens)).toString('utf-8').trim();
    if (decoded.length > 0) chunks.push(decoded);
  }

  enc.free();
  return chunks;
}

// Main embedding + upsert logic
async function embedAndUpsert() {
  const index = pinecone.index(INDEX_NAME);

  console.log('📥 Reading and parsing CSV...');
  const csvRaw = await fs.readFile(CSV_PATH, 'utf-8');
  const courses = await csv().fromString(csvRaw);

  let chunkCount = 0;

  for (const [i, course] of courses.entries()) {
    const {
      subject_code,
      course_number,
      title,
      Days,
      Time,
      Building,
      Room,
      Instructor,
      ['Available Seats']: seatLimit,
      description,
      prerequisites,
      Units
    } = course;

    const code = `${subject_code} ${course_number}`;
    const department = subject_code;

    const formatted = `
Course: ${code}: ${title}
Schedule: Meets on ${Days} at ${Time}
Location: ${Building} ${Room}
Instructor: ${Instructor}
Class Size: ${seatLimit} seats
Description: ${description}
Prerequisites: ${prerequisites || 'None'}
Department: ${department}
Units: ${Units}
`.trim();

    const chunks = await chunkTextTokenStrict(formatted);

    for (const chunk of chunks) {
      const response = await openai.embeddings.create({
        model: EMBEDDING_MODEL,
        input: chunk,
      });

      const vector = response.data[0].embedding;

      await index.upsert([
        {
          id: `course-${code.replace(/\s+/g, '-')}-${chunkCount}`,
          values: vector,
          metadata: {
            code,
            title,
            days: Days,
            time: Time,
            building: Building,
            room: Room,
            instructor: Instructor,
            seatLimit: Number(seatLimit) || 0,
            description,
            prerequisites,
            department,
            units: Units,
            text: chunk,
          },
        },
      ]);

      console.log(`✅ Upserted chunk ${++chunkCount} for ${code}`);
    }
  }

  console.log(`🎉 Done! Total chunks uploaded: ${chunkCount}`);
}

// Run
embedAndUpsert().catch(err => {
  console.error('❌ Ingestion failed:', err);
});
