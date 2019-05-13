from vision_app import app, db
from .views import CityView, AnalysisView

# URLS are declared here

# city view
city_view =  CityView.as_view('city_view')
app.add_url_rule(
    '/cidade/', view_func=city_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/cidade/<int:id>', view_func=city_view, methods=['GET', 'DELETE']
)


# analisys view
analysis_view =  AnalysisView.as_view('analysis_view')
app.add_url_rule(
    '/analise/', view_func=analysis_view, methods=['GET']
)