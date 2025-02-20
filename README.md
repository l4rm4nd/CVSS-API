# CVSS-API

Simple Python Flask API server that returns CVSS scores for CVSS vector strings.

## 🐳 Usage

You can use the provided `docker-compose.yml` or just run:

````
docker run -it -rm -p 5000:5000 ghcr.io/l4rm4nd/cvss-api:latest
````

Afterwards, you can utilize the API server:

````
# query CVSS 2.0 vector
curl "http://127.0.0.1:5000/cvss?vector=CVSS:2.0/AV:N/AC:L/Au:N/C:C/I:C/A:C"
# query CVSS 3.1 vector
curl "http://127.0.0.1:5000/cvss?vector=CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
# query CVSS 4.0 vector
curl "http://127.0.0.1:5000/cvss?vector=CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
````

The API will respond with the following example JSON:

````
{
  "api_version": "0.1.0",
  "cvss_score": 9.8,
  "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
}
````

Combine with an TLS reverse proxy. CORS is already allowed on the Flask application.

> [!TIP]
> For CVSS 4.0, the API server defines `Subsequent System Impact Metrics` as optional.
> 
> Therefore, you can neglect `SC`, `SI` and `SA` from your provided vector string. The backend will automatically set those to `N` (None).
