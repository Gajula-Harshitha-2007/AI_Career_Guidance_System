def recommend_career(
    interest,
    programming,
    problem_solving,
    mathematics,
    ai_interest,
    design,
    security,
    communication
):

    # Convert interest to lowercase
    interest = interest.lower()


    # =========================
    # CAREER SCORING
    # =========================

    scores = {

        "Software Developer":
            (programming * 2) +
            (problem_solving * 2) +
            mathematics,

        "AI / Machine Learning Engineer":
            (programming * 2) +
            mathematics +
            (ai_interest * 2) +
            problem_solving,

        "Data Scientist":
            mathematics * 2 +
            problem_solving +
            (ai_interest * 2) +
            programming,

        "UI/UX Designer":
            (design * 3) +
            (communication * 2) +
            problem_solving,

        "Cybersecurity Analyst":
            (security * 3) +
            programming +
            (problem_solving * 2),

        "Business Analyst":
            (communication * 3) +
            mathematics +
            problem_solving
    }


    # =========================
    # INTEREST BONUS
    # =========================

    interest_bonus = {

        "programming": "Software Developer",

        "art": "UI/UX Designer",

        "design": "UI/UX Designer",

        "art and design": "UI/UX Designer",

        "art_design": "UI/UX Designer",

        "art & design": "UI/UX Designer",

        "art and technology": "UI/UX Designer",

        "art_&_design": "UI/UX Designer",

        "art/design": "UI/UX Designer",

        "art design": "UI/UX Designer",

        "art and creativity": "UI/UX Designer",

        "art_creativity": "UI/UX Designer",

        "data": "Data Scientist",

        "data science": "Data Scientist",

        "artificial intelligence": "AI / Machine Learning Engineer",

        "ai": "AI / Machine Learning Engineer",

        "machine learning": "AI / Machine Learning Engineer",

        "cybersecurity": "Cybersecurity Analyst",

        "security": "Cybersecurity Analyst",

        "business": "Business Analyst",

        "business and management": "Business Analyst",

        "business_management": "Business Analyst"
    }


    # Add bonus for selected interest
    if interest in interest_bonus:

        selected_career = interest_bonus[interest]

        scores[selected_career] += 3


    # =========================
    # FIND RECOMMENDED CAREER
    # =========================

    recommended_career = max(
        scores,
        key=scores.get
    )


    # =========================
    # CAREER DETAILS
    # =========================

    career_details = {

        "Software Developer": {

            "description":
                "Software developers design, build and maintain software applications.",

            "skills":
                [
                    "Python",
                    "Java",
                    "SQL",
                    "Data Structures",
                    "Git"
                ],

            "roadmap":
                [
                    "Learn programming fundamentals",
                    "Learn Data Structures and Algorithms",
                    "Learn SQL and databases",
                    "Build web or software projects",
                    "Learn Git and software development practices"
                ]
        },


        "AI / Machine Learning Engineer": {

            "description":
                "AI and Machine Learning Engineers develop intelligent systems that learn from data.",

            "skills":
                [
                    "Python",
                    "Machine Learning",
                    "Statistics",
                    "SQL",
                    "Deep Learning"
                ],

            "roadmap":
                [
                    "Learn Python",
                    "Learn Mathematics and Statistics",
                    "Learn Machine Learning",
                    "Learn Deep Learning",
                    "Build AI projects"
                ]
        },


        "Data Scientist": {

            "description":
                "Data scientists analyze data and use statistical and machine learning techniques to solve problems.",

            "skills":
                [
                    "Python",
                    "Statistics",
                    "Pandas",
                    "SQL",
                    "Machine Learning"
                ],

            "roadmap":
                [
                    "Learn Python",
                    "Learn Statistics",
                    "Learn Pandas and NumPy",
                    "Learn Data Visualization",
                    "Learn Machine Learning"
                ]
        },


        "UI/UX Designer": {

            "description":
                "UI/UX designers create user-friendly and visually appealing digital experiences.",

            "skills":
                [
                    "Figma",
                    "UI Design",
                    "UX Research",
                    "Wireframing",
                    "Prototyping"
                ],

            "roadmap":
                [
                    "Learn UI/UX fundamentals",
                    "Learn Figma",
                    "Practice wireframing",
                    "Create prototypes",
                    "Build a design portfolio"
                ]
        },


        "Cybersecurity Analyst": {

            "description":
                "Cybersecurity analysts protect computer systems, networks and data from security threats.",

            "skills":
                [
                    "Networking",
                    "Linux",
                    "Cybersecurity",
                    "Python",
                    "Security Tools"
                ],

            "roadmap":
                [
                    "Learn computer networking",
                    "Learn Linux",
                    "Learn cybersecurity fundamentals",
                    "Practice ethical security testing",
                    "Build cybersecurity projects"
                ]
        },


        "Business Analyst": {

            "description":
                "Business analysts use data and business knowledge to help organizations make better decisions.",

            "skills":
                [
                    "Excel",
                    "SQL",
                    "Data Analysis",
                    "Communication",
                    "Problem Solving"
                ],

            "roadmap":
                [
                    "Learn Excel",
                    "Learn SQL",
                    "Learn data analysis",
                    "Improve communication skills",
                    "Work on business case studies"
                ]
        }
    }


    # Get details of recommended career
    details = career_details[recommended_career]


    # Return recommendation
    return recommended_career, scores, details