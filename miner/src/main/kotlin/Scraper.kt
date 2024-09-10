package com.thisismeamir

import java.net.URL

// TODO: We have to describe different Methods
typealias ScrapeMethod = Double

interface Scraper {
    val url: String
    val method: ScrapeMethod

    val result: List<String>
}