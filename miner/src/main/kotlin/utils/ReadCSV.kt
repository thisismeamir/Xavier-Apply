package com.thisismeamir.miner.utils

import java.io.File


fun readCSV(file: File): List<List<String>> {
    val lines = mutableListOf<List<String>>()
    file.readLines().forEach {
        lines.add(it.split(","))
    }
    return lines
}

//fun main() {
//    val file = File("/home/kid-a/Documents/projects/Xavier/miner/src/main/resources/qs-2025-universities.csv")
//    val csvData = readCSV(file)
//
//
//}
