plugins {
    kotlin("jvm")
}

group = "com.thisismeamir"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    // Ktor Client Core and CIO engine
    implementation("io.ktor:ktor-client-core:2.0.0")
    implementation("io.ktor:ktor-client-cio:2.0.0") // CIO engine for HTTP requests

    // Ktor logging and timeout
    implementation("io.ktor:ktor-client-logging:2.0.0")
    // Jsoup for HTML parsing
    implementation("org.jsoup:jsoup:1.14.3")

    // Kotlin coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.0")

    // Ktor dependencies for Kotlin coroutines
    implementation("io.ktor:ktor-client-core-jvm:2.0.0")
    implementation("io.ktor:ktor-client-cio-jvm:2.0.0")
    implementation("io.ktor:ktor-client-logging-jvm:2.0.0")
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}