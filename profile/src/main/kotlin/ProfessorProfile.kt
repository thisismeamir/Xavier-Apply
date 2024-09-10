package com.thisismeamir

data class ProfessorProfile(
    val name: String,
    val lastName: String,
    val university: UniversityProfile,
    val email: String,
    val researchInterests: List<String>,
    val fieldOfStudy: String
)
