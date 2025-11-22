# json_to_english_report.py (Optimized Version)
import os
import json
from groq import Groq
import time
from datetime import datetime

# --- Optimized Settings ---
# GROQ_API_KEY should be passed from streamlit_app.py
JSON_INPUT_FOLDER = 'output'
REPORT_OUTPUT_FOLDER = 'structured_reports'

# --- Optimized Configuration ---
MAX_RETRIES = 3          # کاهش از 5
RETRY_DELAY = 5          # افزایش از 3
MAX_TOKENS = 4000        # کاهش از 8192
TIMEOUT_SECONDS = 60     # کاهش از 180
TEMPERATURE = 0.1

# --- Groq Client ---
try:
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ (Reporter) Groq client initialized successfully.")
except Exception as e:
    client = None
    print(f"❌ (Reporter) Error initializing Groq client: {e}")

class SimplifiedReportGenerator:
    def __init__(self):
        self.client = client
        if not os.path.exists(REPORT_OUTPUT_FOLDER):
            os.makedirs(REPORT_OUTPUT_FOLDER)
            print(f"📁 Created report directory: {REPORT_OUTPUT_FOLDER}")

    def load_json_data(self, json_file_path):
        """Load JSON data from file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"   ❌ Error loading {json_file_path}: {e}")
            return None

    def build_simplified_report_prompt(self, json_data_str: str, filename: str, target_language: str) -> str:
        """Build simplified and optimized prompt"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if target_language == "persian":
            language_instruction = "in Persian (Farsi)"
        else:
            language_instruction = "in English"
        
        return f'''
You are an expert HR analyst. Generate a comprehensive resume assessment report {language_instruction}.

**RESUME DATA:**
```json
{json_data_str}
```

**REQUIRED OUTPUT FORMAT:**

# Resume Assessment Report - [Candidate Name]

## 📋 General Information
- **Full Name:** [name]
- **Date of Birth:** [birth_date or "Not Specified"]
- **Residence:** [residence or "Not Specified"]  
- **Total Experience:** [total_experience_years] years
- **Relevant Experience:** [relevant_experience_years] years
- **Experience Type:** [experience_type]

## 🎯 Overall Assessment
- **Qualification Level:** **[qualification_level]**
- **Calculated Score:** [calculated_score] points
- **Summary:** [summary]

## 📌 Processing Information
- **Source File:** {filename}
- **Processing Date:** {current_time}

---

## 🔍 Detailed Analysis

### 🏭 Industry Competency Analysis
For each industry in competency_industry, explain:
- Why this industry matches candidate's experience
- Specific evidence from resume (job titles, companies, projects)
- Relevance level (High/Medium/Low)
- Technical skills related to this industry

### 🔧 Equipment Competency Analysis
For each equipment in competency_equipment, explain:
- Technical experience with this equipment
- Inspection, maintenance, or operational experience
- Skill level assessment (Expert/Intermediate/Basic)
- Specific projects or roles involving this equipment

### 🎓 Education Analysis
Evaluate education background:
- Degree relevance to technical roles
- Institution quality if known
- Contribution to qualification score
- Additional certifications or training

### 📜 Certifications Analysis
For each qualification, explain:
- Certification validity and level
- Industry recognition and importance
- Point contribution to total score
- Relevance to job requirements

## 📊 Score Breakdown
- **Experience Points:** [detailed calculation]
- **Education Points:** [detailed calculation]  
- **Certification Points:** [detailed calculation]
- **Total Score:** [total] points

## 🎯 Recommendations
- **Hiring Decision:** [Recommend/Consider/Reject]
- **Key Strengths:** [List 3-5 main strengths with specific examples]
- **Development Areas:** [List 2-3 areas for improvement]
- **Best Fit Roles:** [Suggest 2-3 suitable positions based on analysis]

**INSTRUCTIONS:**
1. Provide specific evidence from the resume for each assessment
2. Explain reasoning behind each match/no-match decision
3. Reference actual job titles, companies, and projects mentioned
4. Give detailed explanations, not just lists
5. Focus on technical competencies and relevant experience
6. Write in a professional, analytical tone
7. Be thorough but concise in explanations
'''

    def format_with_groq_retry(self, data, filename, target_language="english"):
        """Generate report with simplified retry logic"""
        if not self.client:
            return "Error: Groq client not initialized."
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        prompt = self.build_simplified_report_prompt(json_str, filename, target_language)
        
        print(f"   📏 Prompt length: {len(prompt)} characters")
        
        # Simplified retry logic
        for attempt in range(MAX_RETRIES):
            try:
                print(f"   🔄 Report generation attempt {attempt + 1}/{MAX_RETRIES}...")
                
                completion = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "system", 
                            "content": f"You are an expert HR analyst specializing in technical resume evaluation. Generate detailed resume assessment reports in {target_language} with specific evidence and explanations for each assessment decision."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    timeout=TIMEOUT_SECONDS
                )
                
                response_content = completion.choices[0].message.content
                print(f"   ✅ Report generated successfully on attempt {attempt + 1}")
                print(f"   📄 Response length: {len(response_content)} characters")
                return response_content
                
            except Exception as e:
                print(f"   ⚠️ Attempt {attempt + 1} failed: {type(e).__name__} - {e}")
                if attempt < MAX_RETRIES - 1:
                    print(f"   ⏳ Waiting {RETRY_DELAY} seconds before retry...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"   ❌ All {MAX_RETRIES} attempts failed")
                    return self.generate_fallback_report(data, filename, target_language)
        
        return self.generate_fallback_report(data, filename, target_language)
    
    def generate_fallback_report(self, data, filename, target_language="english"):
        """Generate basic fallback report when API fails"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        extracted_data = data.get('extracted_data', {})
        analysis = data.get('analysis', {})
        
        name = extracted_data.get('name', 'Name Not Specified')
        birth_date = extracted_data.get('birth_date', 'Not Specified')
        residence = extracted_data.get('residence', 'Not Specified')
        total_exp = extracted_data.get('total_experience_years', 'Not Specified')
        relevant_exp = extracted_data.get('relevant_experience_years', 'Not Specified')
        
        qualification_level = analysis.get('qualification_level', 'Not Specified')
        calculated_score = analysis.get('calculated_score', 'Not Specified')
        summary = analysis.get('summary', 'Complete analysis not available due to API limitations')
        
        if target_language == "persian":
            return f'''
⚠️ **گزارش اضطراری (تحلیل کامل در دسترس نیست)**

# گزارش ارزیابی رزومه - {name}

## 📋 اطلاعات کلی
- **نام کامل:** {name}
- **تاریخ تولد:** {birth_date}
- **محل سکونت:** {residence}
- **کل سابقه کار:** {total_exp} سال
- **سابقه مرتبط:** {relevant_exp} سال

## 🎯 نتیجه ارزیابی
- **سطح صلاحیت:** {qualification_level}
- **امتیاز محاسبه شده:** {calculated_score}
- **خلاصه:** {summary}

## 📌 اطلاعات پردازش
- **فایل منبع:** {filename}
- **تاریخ پردازش:** {current_time}
- **وضعیت:** گزارش ساده به دلیل محدودیت API

---
**توجه:** این گزارش ساده است. برای تحلیل کامل، لطفاً مجدداً تلاش کنید.
'''
        else:
            return f'''
⚠️ **FALLBACK REPORT (Complete Analysis Unavailable)**

# Resume Assessment Report - {name}

## 📋 General Information
- **Full Name:** {name}
- **Date of Birth:** {birth_date}
- **Residence:** {residence}
- **Total Experience:** {total_exp} years
- **Relevant Experience:** {relevant_exp} years

## 🎯 Assessment Result
- **Qualification Level:** {qualification_level}
- **Calculated Score:** {calculated_score}
- **Summary:** {summary}

## 📌 Processing Information
- **Source File:** {filename}
- **Processing Date:** {current_time}
- **Status:** Simplified report due to API limitations

---
**Note:** This is a simplified report. Please try again for complete analysis.
'''

    def process_all_json_files(self, target_language="english"):
        """Process all JSON files and generate reports"""
        if not os.path.exists(JSON_INPUT_FOLDER):
            print(f"❌ Input folder '{JSON_INPUT_FOLDER}' not found.")
            return

        json_files = [f for f in os.listdir(JSON_INPUT_FOLDER) if f.endswith('.json')]
        if not json_files:
            print(f"❌ No JSON files found in '{JSON_INPUT_FOLDER}'.")
            return
            
        print(f"--- Starting Optimized Report Generation in {target_language.capitalize()} ---")
        print(f"🔄 Configuration: {MAX_RETRIES} attempts, {RETRY_DELAY}s delay, {MAX_TOKENS} max tokens")

        successful_reports = 0
        failed_reports = 0
        
        for json_file in json_files:
            print(f"\n🔄 Processing: {json_file}")
            json_path = os.path.join(JSON_INPUT_FOLDER, json_file)
            data = self.load_json_data(json_path)
            if data is None:
                failed_reports += 1
                continue
            
            source_filename = data.get('metadata', {}).get('source_file', json_file)
            report = self.format_with_groq_retry(data, source_filename, target_language)
            
            base_name = os.path.splitext(json_file)[0]
            report_path = os.path.join(REPORT_OUTPUT_FOLDER, f"{base_name}_{target_language}_report.txt")
            
            try:
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"   ✅ {target_language.capitalize()} report saved to: {report_path}")
                successful_reports += 1
            except Exception as e:
                print(f"   ❌ Failed to save report file {report_path}: {e}")
                failed_reports += 1
                
            # Small delay between requests
            time.sleep(2)
            
        print(f"\n\n--- Report Generation Complete ---")
        print(f"📊 Results: {successful_reports} successful, {failed_reports} failed")
        if failed_reports > 0:
            print(f"⚠️ {failed_reports} reports had issues but fallback reports were generated")

def main():
    """Main function to run the report generator"""
    if client is None:
        print("❌ Aborting due to Groq client initialization failure.")
        return
    
    # تنظیم زبان گزارش
    LANGUAGE_TO_GENERATE = "english"  # تغییر به "persian" در صورت نیاز
    
    generator = SimplifiedReportGenerator()
    generator.process_all_json_files(target_language=LANGUAGE_TO_GENERATE)

if __name__ == "__main__":
    main()