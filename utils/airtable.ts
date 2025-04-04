import Airtable from 'airtable';

// Create Airtable instances with different API keys
const mainAirtable = new Airtable({
  apiKey: process.env.NEXT_PUBLIC_AIRTABLE_API_KEY
});

const descriptionsAirtable = new Airtable({
  apiKey: process.env.NEXT_PUBLIC_AIRTABLE_Descriptions_API_KEY
});

// Create base instances for Courses, Sections, and Descriptions
const coursesBase = mainAirtable.base(process.env.NEXT_PUBLIC_AIRTABLE_BASE_ID_Courses!);
const sectionsBase = mainAirtable.base(process.env.NEXT_PUBLIC_AIRTABLE_BASE_ID_Sections!);
const descriptionsBase = descriptionsAirtable.base(process.env.NEXT_PUBLIC_AIRTABLE_BASE_ID_Descriptions!);

// Get table references
export const sectionsTable = sectionsBase(process.env.NEXT_PUBLIC_AIRTABLE_TABLE_NAME_Sections!);
export const coursesTable = coursesBase(process.env.NEXT_PUBLIC_AIRTABLE_TABLE_NAME_Courses!);
export const descriptionsTable = descriptionsBase(process.env.NEXT_PUBLIC_AIRTABLE_TABLE_NAME_Descriptions!);

interface Course {
  id: string;
  'Course Number': string;
  'Subject Code': string;
  'Course Name': string;
  'Units': string;
  'Sections': string[];
}

interface Section {
  id: string;
  'Subject Code': string;
  'Course Link': string | string[];
  'Meeting Type': string;
  'Time': string;
  'Building': string;
  'Room': string;
  'Instructor': string;
  'Available Seats': number;
  'Seat Limit': string;
  'Days': string;
}

interface CourseDescription {
  id: string;
  code: string;
  title: string;
  units: number;
  description: string;
  prerequisites: string;
}

export function getMinifiedRecord(record: any) {
  return {
    id: record.id,
    ...record.fields,
  }
}

export function getMinifiedRecords(records: ReadonlyArray<any> | any[]) {
  return records.map((record) => getMinifiedRecord(record))
}

export async function fetchRecords() {
  try {
    console.log('🔄 Fetching courses...');
    const courseRecords = await coursesTable.select({}).all();
    const courses = getMinifiedRecords([...courseRecords]) as Course[];
    console.log('🧠 All course IDs:', courses.map(c => c.id));
    console.log(`✅ Courses fetched: ${courses.length}`);

    console.log('🔄 Fetching sections...');
    const allSectionRecords = await sectionsTable.select({}).all();
    const allSections = getMinifiedRecords([...allSectionRecords]) as Section[];
    console.log(`✅ Sections fetched: ${allSections.length}`);

    const lectureSections = allSections.filter(section =>
      section['Meeting Type'].toLowerCase() === 'remote' &&
      !section['Building'].includes('RCLAS')
    );

    


    const combinedData = lectureSections.map(lectureSection => {
      // 🔍 Normalize 'Course Link' — handles stringified arrays
      let rawLink = lectureSection['Course Link'];
      if (typeof rawLink === 'string' && rawLink.startsWith("['")) {
        try {
          rawLink = JSON.parse(rawLink.replace(/'/g, '"'));
        } catch (err) {
          console.warn('⚠️ Could not parse Course Link:', rawLink);
        }
      }
      const courseLink = Array.isArray(rawLink) ? rawLink[0] : rawLink;

      if (!courseLink) {
        console.log('⚠️ Section missing Course Link:', lectureSection);
        return null;
      }

      const course = courses.find(c => c.id === courseLink);
      if (!course) {
        console.log('❌ Course not found for Link:', courseLink);
        return null;
      }

      const courseName = course['Course Name']?.toLowerCase() ?? '';
      if (courseName.includes('lab') || courseName.includes('laboratory')) {
        return null;
      }

      let seatLimit = parseInt(lectureSection['Seat Limit'] || '0');

      if (seatLimit === 0) {
        const discussionSections = allSections.filter(section => {
          let link = section['Course Link'];
          if (typeof link === 'string' && link.startsWith("['")) {
            try {
              link = JSON.parse(link.replace(/'/g, '"'));
            } catch {}
          }
          const sectionCourseLink = Array.isArray(link) ? link[0] : link;

          return section['Meeting Type'] === 'Discussion' &&
            section['Subject Code'] === lectureSection['Subject Code'] &&
            sectionCourseLink === courseLink;
        });

        seatLimit = discussionSections.reduce((total, section) => {
          const limit = parseInt(section['Seat Limit'] || '0');
          return total + limit;
        }, 0);
      }

      const processed = {
        id: lectureSection.id,
        courseId: course.id,
        courseCode: `${lectureSection['Subject Code']} ${course['Course Number']}`,
        courseName: course['Course Name'],
        professor: lectureSection['Instructor'],
        building: lectureSection['Building'],
        room: lectureSection['Room'],
        capacity: seatLimit,
        time: lectureSection['Time'],
        days: lectureSection['Days'],
        meetingType: lectureSection['Meeting Type'],
      };
      return processed;
    }).filter(Boolean);

    return { records: combinedData, error: null };
  } catch (error) {
    console.error('❌ Error fetching Airtable records:', error);
    return {
      records: [],
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
};


export async function fetchCourseDescriptions() {
  try {
    const records = await descriptionsTable.select({}).all();
    const minifiedRecords = getMinifiedRecords(records);
    console.log('🧪 Normalized description keys:', minifiedRecords.map(d => d.code));

    return {
      records: minifiedRecords as CourseDescription[],
      error: null
    }
  } catch (error) {
    console.error('Error fetching course descriptions:', error)
    return {
      records: [],
      error: error as Error
    }
  }
};
