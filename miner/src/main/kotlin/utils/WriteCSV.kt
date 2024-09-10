package com.thisismeamir.miner.utils

import java.io.File
import java.io.FileWriter

fun List<List<String>>.writeCSV(dir: String, fileName: String, columns: List<String>): Unit {
    val file = File(dir, fileName)

    // Ensure the directory exists
    file.parentFile.mkdirs()

    FileWriter(file).use { writer ->
        // Write the column headers
        writer.append(columns.joinToString(","))
        writer.append("\n")

        // Write each row of data
        this.forEach { row ->
            writer.append(row.joinToString(","))
            writer.append("\n")
        }
    }
}

//fun main() {
//    val data: List<List<String>> = listOf(
//        listOf("1", "Alice", "25"),
//        listOf("2", "Bob", "30"),
//        listOf("3", "Charlie", "35")
//    )
//
//    val columns = listOf("ID", "Name", "Age")
//
//    // Specify directory and filename
//    val dir = "miner/src/main/resources"
//    val fileName = "output.csv"
//
//    // Write the CSV
//    data.writeCSV(dir, fileName, columns)
//
//    println("CSV file written successfully!")
//}
