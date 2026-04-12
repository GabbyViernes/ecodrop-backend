"""
URL configuration for ecodrop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from core.views import profile_view


def home(request):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ecodrop API</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #27ae60;
            }}
            .links {{
                margin-top: 20px;
            }}
            .link-group {{
                margin: 15px 0;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Ecodrop API</h1>
            <p>Welcome to the Ecodrop waste management system API.</p>
            
            <div class="links">
                <div class="link-group">
                    <strong>Authentication:</strong><br>
                    • <a href="/accounts/login/">Login (Browser)</a><br>
                    • <a href="/api/register/">Register API</a><br>
                    • <a href="/api/login/">Login API (Token)</a>
                </div>
                
                <div class="link-group">
                    <strong>Profile:</strong><br>
                    • <a href="/accounts/profile/">View My Profile</a><br>
                    • <a href="/api/profile/">Profile API (Token Auth)</a>
                </div>
                
                <div class="link-group">
                    <strong>API Endpoints:</strong><br>
                    • <a href="/api/">API Root</a><br>
                    • <a href="/api/bins/">Smart Bins</a><br>
                    • <a href="/api/alerts/">Maintenance Alerts</a>
                </div>
                
                <div class="link-group">
                    <strong>Admin:</strong><br>
                    • <a href="/admin/">Admin Panel</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile_view, name='web-profile'),
]
