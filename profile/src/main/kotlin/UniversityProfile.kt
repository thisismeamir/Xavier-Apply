package com.thisismeamir

import java.io.File

data class UniversityProfile(
    val name: String,
    val acronym: String,
    val rank: Int,

    val country: String,
    val region: String,
    val size: String,

    val professors: List<ProfessorProfile>,
    val application: Application
){

    fun toMarkdown(): File {
        TODO()
    }

    fun professorsToExcel(): File {
        TODO()
    }
}
