def suggest_projects(language, level):
    suggestions = {
        "Python": [
            "Build a Flask REST API",
            "Contribute to a Python open-source repo",
            "Create a CLI tool"
        ],
        "JavaScript": [
            "Build a React app",
            "Contribute to a JS repo",
            "Create a browser extension"
        ]
    }

    return suggestions.get(language, ["Explore open source projects"])