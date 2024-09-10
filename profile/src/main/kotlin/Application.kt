package com.thisismeamir

import com.thisismeamir.types.LanguageProficiencyType
import java.util.Date

data class Application(

    // general information
    val name: String,
    val deadLine: Date,
    val description: List<String>,

    // requirements
    val requiresSOP: Boolean,
    val requiresCV: Boolean,
    val requiresLanguageProficiency: Pair<LanguageProficiencyType, Double>,

)
