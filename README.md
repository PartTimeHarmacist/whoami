# whoami

This is a streamlit application that aims to serve as the landing page for my (somewhat) professional portfolio.
Since most of my work as a data engineer is cordoned off behind intellectual property, the projects and data showcased
in this repository are designed to be at least _somewhat_ useful while utilizing publicly available data.

## This Application
It's basically just a fancy extended resume that uses streamlit.

This application itself is designed to be data powered in nearly all aspects.
In part because it showcases how I use streamlit, but also because it makes it
just a bit more versatile later down the line.

The `Greeting`, `About Me` and `Questions and Answers` sections are all dynamically loaded
from a postgres database in my kubernetes cluster.  The `Example Projects` section is the only
section that isn't loaded from a database, as it's a bit more involved than a simple line or two of text.  In the future
it will likely become a markdown file that is read from instead.

The real code and examples are all in the `Example Projects` links though.  Right now, it lists out the following:
- [Warframe Drops Application](https://warframe.datadumplings.cloud) - [[source]](https://github.com/PartTimeHarmacist/whoami/blob/main/src/pages/Warframe_Drops_Application.py)
- [Apache Airflow Deployment](https://airflow.datadumplings.cloud) - [[source]](https://github.com/PartTimeHarmacist/datadumplings_dags)
- [Apache Superset Deployment](https://superset.datadumplings.cloud)
- Teamcity Deployment
- Private Gitea Deployment
- Private Minio (S3) Deployment

With more to come as I add to it.