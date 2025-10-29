import os
import sqlite3
import PyPDF2
from docx import Document
import webbrowser
import re
import os

print("📁 Database path:", os.path.abspath("job_finder.db"))

# ------------------ DATABASE SETUP ------------------
conn = sqlite3.connect("job_finder.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    phone TEXT,
    password TEXT,
    resume TEXT
)
""")

# Job providers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS job_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
#coursse provider
cursor.execute("""
CREATE TABLE IF NOT EXISTS course_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    phone TEXT,       
    email TEXT,       
    address TEXT      
)
""")               


cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    course_name TEXT,
    duration TEXT,
    description TEXT,
    link TEXT,
    FOREIGN KEY(provider_id) REFERENCES course_providers(id)
)
""")


# Jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    job_title TEXT,
    company_name TEXT,
    job_description TEXT,
    location TEXT,
    experience TEXT,
    FOREIGN KEY(provider_id) REFERENCES job_providers(id)
)
""")

# Applied candidates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applied_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    job_id INTEGER,
    resume TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
               
)
""")

# Courses table

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    course_name TEXT,
    duration TEXT,
    description TEXT,
    link TEXT,
    FOREIGN KEY (provider_id) REFERENCES course_providers(id)
)
""")

# 7️⃣ Course recommendations table
cursor.execute("""
CREATE TABLE IF NOT EXISTS course_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    reason TEXT,               -- e.g. "Skill not found in resume"
    recommendation_type TEXT,  -- 'matching' or 'not_in_resume'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")

# ✅ Save all changes and close
conn.commit()
conn.close()


# ------------------ REGISTRATION FUNCTIONS ------------------
def User_Register():
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    phone = input("Enter Phone: ")
    password = input("Enter Password: ")
    confirm = input("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        conn.close()
        return

    try:
        cursor.execute("INSERT INTO users (username, phone, password) VALUES (?, ?, ?)",
                       (username, phone, password))
        conn.commit()
        print(f"✅ User {username} registered successfully!")
        post_registration_login()
    except Exception as e:
        print(f"⚠ Error: {e}")
    finally:
        conn.close()


def JobProvider_Register():
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    confirm = input("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        conn.close()
        return

    try:
        cursor.execute("INSERT INTO job_providers (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"✅ Job Provider {username} registered successfully!")
        post_registration_login()
    except Exception as e:
        print(f"⚠ Error: {e}")
    finally:
        conn.close()


def CourseProvider_Register():
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    confirm = input("Confirm Password: ")
    

    if password != confirm:
        print("❌ Passwords do not match.")
        conn.close()
        return

    try:
        cursor.execute("INSERT INTO course_providers (username, password, phone, email) VALUES (?, ?, ?, ?)", 
               (username, password, phone, email))

        conn.commit()
        print(f"✅ Course Provider {username} registered successfully!")
        post_registration_login()
    except Exception as e:
        print(f"⚠ Error: {e}")
    finally:
        conn.close()

# ------------------ POST-REGISTRATION ------------------
def post_registration_login():
    while True:
        print("\nWhat do you want to do next?")
        print("1. Login")
        print("2. Exit")
        choice = input("Select your choice: ")
        if choice == "1":
            User_Login()
            break
        elif choice == "2":
            print("Thank you for using Job Finder!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ------------------ LOGIN FUNCTIONS ------------------
def User_Login():
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Check User
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"✅ Welcome {username} (User)")
        user_dashboard(username)
        conn.close()
        return

    # Check Job Provider
    cursor.execute("SELECT * FROM job_providers WHERE username=? AND password=?", (username, password))
    job_provider = cursor.fetchone()
    if job_provider:
        print(f"✅ Welcome {username} (Job Provider)")
        job_provider_dashboard(username)
        conn.close()
        return

    # Check Course Provider
    cursor.execute("SELECT * FROM course_providers WHERE username=? AND password=?", (username, password))
    course_provider = cursor.fetchone()
    if course_provider:
        print(f"✅ Welcome {username} (Course Provider)")
        course_provider_dashboard(username)
        conn.close()
        return

    # Admin Login
    if username.lower() == "admin" and password == "admin":
        print("✅ Admin Login Successful!")
        admin_dashboard()
        conn.close()
        return

    print("❌ Invalid Username or Password.")
    conn.close()

# ------------------ DASHBOARDS ------------------
def user_dashboard(username):
    while True:
        print("\n--- User Dashboard ---")
        print("1. Upload/Update Resume")
        print("2. View Matching Jobs")
        print("3. Apply for Job")
        print("4. View Courses NOT in Resume (new skills)")
        print("5. Logout")

        choice = input("Select: ")
        if choice == "1":
            upload_resume(username)
        elif choice == "2":
            view_jobs_matching_resume(username)
        elif choice == "3":
            apply_for_job(username)
        elif choice == "4":
            view_courses_not_in_resume(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("❌ Invalid choice.")



def job_provider_dashboard(username):
    while True:
        print("\n--- Job Provider Dashboard ---")
        print("1. Add Job")
        print("2. View Jobs & Applied Candidates")
        print("3. Logout")

        choice = input("Select: ")
        if choice == "1":
            add_job(username)
        elif choice == "2":
            view_jobs_and_candidates(username)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("❌ Invalid choice.")


def course_provider_dashboard(username):
    while True:
        print("\n--- 📚 Course Provider Dashboard ---")
        print("1. ➕ Add Course")
        print("2. 👀 View My Courses")
        print("3. 🚪 Logout")

        choice = input("Select an option: ")

        if choice == "1":
            add_course(username)
        elif choice == "2":
            view_my_courses(username)

        elif choice == "3":
            print("✅ Logged out successfully.")
            break
        else:
            print("❌ Invalid choice. Please try again.")



def admin_dashboard():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View All Users")
        print("2. View All Job Providers")
        print("3. View All Course Providers")
        print("4. Logout")
        choice = input("Select: ")
        conn = sqlite3.connect("job_finder.db")
        cursor = conn.cursor()
        if choice == "1":
            cursor.execute("SELECT username, phone FROM users")
            users = cursor.fetchall()
            print("\n--- Users ---")
            for u in users:
                print(f"Username: {u[0]} | Phone: {u[1]}")
        elif choice == "2":
            cursor.execute("SELECT username FROM job_providers")
            providers = cursor.fetchall()
            print("\n--- Job Providers ---")
            for p in providers:
                print(f"Username: {p[0]}")
        elif choice == "3":
            cursor.execute("SELECT username FROM course_providers")
            providers = cursor.fetchall()
            print("\n--- Course Providers ---")
            for p in providers:
                print(f"Username: {p[0]}")
        elif choice == "4":
            print("Logging out from Admin...")
            conn.close()
            break
        else:
            print("❌ Invalid choice.")
        conn.close()

# ------------------ FUNCTION IMPLEMENTATIONS ------------------
def upload_resume(username):
    path = input("Enter resume path (.txt/.pdf/.docx): ")
    if not os.path.exists(path):
        print("❌ File not found.")
        return
    text = ""
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == ".pdf":
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        elif ext == ".docx":
            doc = Document(path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            print("❌ Unsupported file type.")
            return
        conn = sqlite3.connect("job_finder.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET resume=? WHERE username=?", (text, username))
        conn.commit()
        conn.close()
        print("✅ Resume uploaded successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")


def view_jobs_matching_resume(username):
    import re
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    cursor.execute("SELECT resume FROM users WHERE username=?", (username,))
    resume = cursor.fetchone()
    if not resume or not resume[0]:
        print("⚠ Please upload your resume first.")
        conn.close()
        return

    resume_text = resume[0].lower()

    # Extract keywords from resume (basic approach: words with letters/numbers)
    resume_keywords = set(re.findall(r'\b\w+\b', resume_text))

    cursor.execute("""
        SELECT jp.username, j.job_title, j.company_name, j.job_description, j.location, j.experience
        FROM jobs j
        JOIN job_providers jp ON j.provider_id = jp.id
    """)
    jobs = cursor.fetchall()
    matched = False

    for provider, title, company, desc, loc, exp in jobs:
        # Combine job details into one string
        job_text = (title + " " + desc + " " + exp).lower()
        job_keywords = set(re.findall(r'\b\w+\b', job_text))

        # Count how many resume keywords are actually in job keywords
        common_skills = resume_keywords & job_keywords
        if common_skills:
            print(f"\n💼 {title} at {company} (Provider: {provider})")
            print(f"📍 {loc} | 📝 {desc} | 🧠 Exp: {exp}")
            print(f"🔹 Matching Keywords: {', '.join(common_skills)}")
            matched = True

    if not matched:
        print("⚠ No matching jobs found.")

    conn.close()



def apply_for_job(username):
    import re
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    # Fetch user's resume
    cursor.execute("SELECT id, resume FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if not user:
        print("❌ User not found.")
        conn.close()
        return
    user_id, resume_text = user

    if not resume_text:
        print("⚠ Please upload your resume first.")
        conn.close()
        return

    # Extract resume keywords
    resume_keywords = set(re.findall(r'\b\w+\b', resume_text.lower()))

    # Fetch all jobs with provider info
    cursor.execute("""
        SELECT jp.username, j.id, j.job_title, j.company_name, j.job_description, j.location, j.experience
        FROM jobs j
        JOIN job_providers jp ON j.provider_id = jp.id
    """)
    jobs = cursor.fetchall()

    # Filter jobs matching resume keywords
    matching_jobs = []
    for provider, job_id, title, company, desc, loc, exp in jobs:
        job_keywords = set(re.findall(r'\b\w+\b', (title + " " + desc + " " + exp).lower()))
        if resume_keywords & job_keywords:
            matching_jobs.append((provider, job_id, title, company, desc, loc, exp))

    # If no jobs match, show message and exit
    if not matching_jobs:
        print("⚠ No jobs match your resume currently. Please try again later.")
        conn.close()
        return

    # Display matching jobs
    print("\n💼 Matching Jobs:")
    for idx, (provider, job_id, title, company, desc, loc, exp) in enumerate(matching_jobs, start=1):
        print(f"{idx}. {title} at {company} (Provider: {provider})")
        print(f"   📍 {loc} | 📝 {desc} | 🧠 Exp: {exp}")

    # Ask user to select a job by number
    try:
        choice = int(input("Select the job number to apply: "))
        if choice < 1 or choice > len(matching_jobs):
            print("❌ Invalid selection.")
            conn.close()
            return
    except ValueError:
        print("❌ Invalid input. Enter a number.")
        conn.close()
        return

    selected_job = matching_jobs[choice - 1]
    selected_job_id = selected_job[1]
    selected_provider = selected_job[0]
    selected_title = selected_job[2]

    # Apply for the selected job
    cursor.execute(
        "INSERT INTO applied_candidates (user_id, job_id, resume) VALUES (?, ?, ?)",
        (user_id, selected_job_id, resume_text)
    )
    conn.commit()
    conn.close()
    print(f"✅ Applied for '{selected_title}' at {selected_provider}!")



def add_job(username):
    title = input("Job Title: ")
    company = input("Company Name: ")
    desc = input("Job Description: ")
    loc = input("Location: ")
    exp = input("Experience: ")

    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM job_providers WHERE username=?", (username,))
    provider = cursor.fetchone()
    if not provider:
        print("❌ Provider not found.")
        conn.close()
        return
    provider_id = provider[0]
    cursor.execute("INSERT INTO jobs (provider_id, job_title, company_name, job_description, location, experience) VALUES (?, ?, ?, ?, ?, ?)",
                   (provider_id, title, company, desc, loc, exp))
    conn.commit()
    conn.close()
    print("✅ Job added successfully!")


def view_jobs_and_candidates(username):
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    try:
        # Get the provider's ID
        cursor.execute("SELECT id FROM job_providers WHERE username=?", (username,))
        provider = cursor.fetchone()
        if not provider:
            print("❌ Provider not found.")
            return
        provider_id = provider[0]

        # Get all jobs posted by this provider
        cursor.execute("SELECT id, job_title, company_name FROM jobs WHERE provider_id=?", (provider_id,))
        jobs = cursor.fetchall()

        if not jobs:
            print("ℹ️ You haven't posted any jobs yet.")
            return

        for job_id, title, company in jobs:
            print(f"\n💼 Job: {title} | Company: {company}")

            # Get candidates who applied to this job
            cursor.execute("""
                SELECT u.username FROM applied_candidates a
                JOIN users u ON a.user_id = u.id
                WHERE a.job_id=?
            """, (job_id,))
            candidates = cursor.fetchall()

            if candidates:
                print("Applied Candidates:")
                for c in candidates:
                    print(f"- {c[0]}")
            else:
                print("No candidates have applied yet.")

    except sqlite3.Error as e:
        print("❌ Database error:", e)

    finally:
        conn.close()


import sqlite3

def add_course(username):
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    # Get the provider ID from username
    cursor.execute("SELECT id FROM course_providers WHERE username=?", (username,))
    provider = cursor.fetchone()

    if not provider:
        print("⚠ Course provider not found.")
        conn.close()
        return

    provider_id = provider[0]

    # Get course details
    course_name = input("📘 Enter Course Name: ")
    duration = input("⏳ Enter Duration: ")
    description = input("📝 Enter Description: ")
    link = input("🔗 Enter Course Link (optional): ")

    # Insert course data
    cursor.execute("""
        INSERT INTO courses (provider_id, course_name, duration, description, link)
        VALUES (?, ?, ?, ?, ?)
    """, (provider_id, course_name, duration, description, link))

    # ✅ Important: Save changes
    conn.commit()
    print("✅ Course added successfully!")

    conn.close()

  



import sqlite3
import webbrowser

def main_menu():
    while True:
        print("\n👩‍💼.....Welcome to Job Finder.....👨‍💼🌈\n")
        print("1. Admin Login")
        print("2. User Registration")
        print("3. Job Provider Registration")
        print("4. Course Provider Registration")
        print("5. Login (Any Role)")
        print("6. Exit")

        choice = input("Select your choice: ")

        if choice == "1" or choice == "5":
            User_Login()
        elif choice == "2":
            User_Register()
        elif choice == "3":
            JobProvider_Register()
        elif choice == "4":
            CourseProvider_Register()
        elif choice == "6":
            print("Thank you for using Job Finder!")
            break
        else:
            print("❌ Invalid option selected.")

# Updated course recommendations



def view_courses_not_in_resume(username):
    conn = sqlite3.connect("job_finder.db")
    cursor = conn.cursor()

    # Get resume
    cursor.execute("SELECT resume FROM users WHERE username=?", (username,))
    resume = cursor.fetchone()

    if not resume or not resume[0]:
        print("⚠ Please upload your resume first.")
        conn.close()
        return

    # Clean and normalize resume text
    resume_text = resume[0].lower()
    resume_text = re.sub(r'[^\w\s]', '', resume_text)  # remove punctuation
    resume_words = set(resume_text.split())

    # Get all courses with provider details
    cursor.execute("""
        SELECT c.id, cp.username, cp.phone, c.course_name, c.duration, c.description, c.link
        FROM courses c
        JOIN course_providers cp ON c.provider_id = cp.id
    """)
    courses = cursor.fetchall()

    unmatched_courses = []

    # Match only by course name
    for cid, provider, phone, name, duration, desc, link in courses:
        course_name = re.sub(r'[^\w\s]', '', name.lower())
        course_words = set(course_name.split())

        # If none of the course name words are in the resume, recommend it
        if not any(word in resume_words for word in course_words):
            unmatched_courses.append((cid, provider, phone, name, duration, desc, link))

    # Display recommendations
    if unmatched_courses:
        print("\n🎯 Courses NOT found in your resume (recommended for upskilling):\n")
        for cid, provider, phone, name, dur, desc, link in unmatched_courses:
            print(f"🆔 ID: {cid}")
            print(f"📚 {name} | Provider: {provider} | Duration: {dur}")
            print(f"   📝 Description: {desc}")
            if link and link.strip():
                print(f"   🔗 Course Link: {link}")
            else:
                print(f"   💬 WhatsApp: https://wa.me/{phone}")
            print("-" * 60)

        # Ask user which course to contact
        try:
            selected_id = int(input("\nEnter the ID of the course you want to contact via WhatsApp: "))
            selected_course = next((c for c in unmatched_courses if c[0] == selected_id), None)

            if selected_course:
                provider_phone = selected_course[2]
                print(f"📞 Opening WhatsApp chat with provider for course '{selected_course[3]}'...")
                webbrowser.open(f"https://wa.me/{provider_phone}")
            else:
                print("❌ Invalid ID selected.")
        except ValueError:
            print("⚠ Please enter a valid numeric course ID.")
    else:
        print("✅ Your resume already covers all available course topics!")

    conn.close()








# def view_course_applicants(provider_username):
#     conn = sqlite3.connect("job_finder.db")
#     cursor = conn.cursor()

#     # Get provider ID
#     cursor.execute("SELECT id FROM course_providers WHERE username=?", (provider_username,))
#     provider = cursor.fetchone()
#     if not provider:
#         print("❌ Provider not found.")
#         conn.close()
#         return
#     provider_id = provider[0]

#     # Get courses by provider
#     cursor.execute("SELECT id, course_name FROM courses WHERE provider_id=?", (provider_id,))
#     courses = cursor.fetchall()

#     if not courses:
#         print("⚠ No courses found.")
#         conn.close()
#         return

#     for cid, cname in courses:
#         print(f"\n📚 Course: {cname}")
#         cursor.execute("""
#             SELECT u.username FROM course_applications ca
#             JOIN users u ON ca.user_id = u.id
#             WHERE ca.course_id=?
#         """, (cid,))
#         users = cursor.fetchall()
#         if users:
#             print("Applied Users:")
#             for u in users:
#                 print(f"- {u[0]}")
#         else:
#             print("No users applied yet.")

#     conn.close()


def view_my_courses(username):
    try:
        # Connect to the database inside the function
        conn = sqlite3.connect("job_finder.db")
        cursor = conn.cursor()

        # 1️⃣ Get provider id
        cursor.execute("SELECT id FROM course_providers WHERE username=?", (username,))
        provider = cursor.fetchone()
        if not provider:
            print("⚠ Course provider not found.")
            return

        provider_id = provider[0]

        # 2️⃣ Fetch all courses added by this provider
        cursor.execute("""
            SELECT course_name, duration, description, link
            FROM courses
            WHERE provider_id=?
        """, (provider_id,))
        courses = cursor.fetchall()

        # 3️⃣ Display results
        if not courses:
            print("⚠ You have not added any courses yet.")
        else:
            print(f"\n📚 Courses for {username}:")
            for idx, (name, duration, desc, link) in enumerate(courses, start=1):
                print(f"{idx}. {name} | Duration: {duration} | Description: {desc} | Link: {link}")

    except sqlite3.Error as e:
        print("❌ Database error:", e)

    finally:
        # Always close connection after use
        conn.close()






# ------------------ MAIN MENU ------------------
print("👩‍💼.....Welcome to Job Finder.....👨‍💼🌈\n")
print("1. Admin Login")
print("2. User Registration")
print("3. Job Provider Registration")
print("4. Course Provider Registration")
print("5. Login (Any role)")
print("6. Exit")

choice = input("Select your choice: ")

if choice == "1":
    User_Login()  # Admin login handled inside
elif choice == "2":
    User_Register()
elif choice == "3":
    JobProvider_Register()
elif choice == "4":
    CourseProvider_Register()
elif choice == "5":
    User_Login()
elif choice == "6":
    print("Thank you for using Job Finder!")
else:
    print("❌ Invalid option selected.")



    # how to talk to 