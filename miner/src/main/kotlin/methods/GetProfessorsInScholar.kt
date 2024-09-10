package methods

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element

suspend fun scrapeAllAuthorsFromUniversity(label: String, universityName: String): List<Map<String, String?>> {
    val client = HttpClient(CIO)

    val params = mapOf(
        "view_op" to "search_authors",
        "mauthors" to "label:$label \"$universityName\"",
        "hl" to "en",
        "astart" to "0"
    )

    val headers = mapOf(
        "User-Agent" to "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36"
    )

    val profileResults = mutableListOf<Map<String, String?>>()

    var profilesIsPresent = true
    var currentParams = params.toMutableMap()

    while (profilesIsPresent) {
        val response: HttpResponse = client.get("https://scholar.google.com/citations") {
            headers { headers.forEach { (key, value) -> header(key, value) } }
            url {
                currentParams.forEach { (key, value) -> parameters.append(key, value) }
            }
        }
        val html = response.bodyAsText()
        val doc: Document = Jsoup.parse(html)

        println("extracting authors at page #${currentParams["astart"]}.")

        doc.select(".gs_ai_chpr").forEach { profile: Element ->
            val name = profile.select(".gs_ai_name a").text()
            val link = "https://scholar.google.com${profile.select(".gs_ai_name a").attr("href")}"
            val affiliations = profile.select(".gs_ai_aff").text()
            val email = profile.select(".gs_ai_eml").text()
            val citedBy = profile.select(".gs_ai_cby").text()
            val interests = profile.select(".gs_ai_one_int").map { it.text() }

            profileResults.add(
                mapOf(
                    "profile_name" to name,
                    "profile_link" to link,
                    "profile_affiliations" to affiliations,
                    "profile_email" to email,
                    "profile_city_by_count" to citedBy,
                    "profile_interests" to interests.joinToString(", ")
                )
            )
        }

        val nextPageToken = doc.select("button.gs_btnPR").attr("onclick").let {
            Regex("after_author\\x3d(.*)\\x26").find(it)?.groupValues?.get(1)
        }

        if (nextPageToken != null) {
            currentParams["after_author"] = nextPageToken
            currentParams["astart"] = (currentParams["astart"]!!.toInt() + 10).toString()
        } else {
            profilesIsPresent = false
        }
    }

    client.close()
    return profileResults
}

// Example usage
suspend fun main() {
    val results = scrapeAllAuthorsFromUniversity("physics", "Michigan University")
    println(results)
}