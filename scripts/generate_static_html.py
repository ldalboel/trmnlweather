#!/usr/bin/env python3
"""
Generate a static HTML file with embedded trains and calendar data.
This ensures TRMNL and other simple browsers get the data without relying on JS loading.
"""

import json
import os
from pathlib import Path

def generate_static_html():
    """Generate index.html with embedded data from trains-data.js and calendar-data.js"""
    
    script_dir = Path(__file__).parent.parent
    
    # Read the template HTML (NOT the generated index.html)
    template_file = script_dir / 'index.template.html'
    if not template_file.exists():
        print("Error: index.template.html not found")
        return
    
    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Read trains data
    trains_data = {}
    trains_file = script_dir / 'trains-data.js'
    if trains_file.exists():
        with open(trains_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract JSON from "window.trainsData = {...};"
            if 'window.trainsData = ' in content:
                json_str = content.replace('window.trainsData = ', '').rstrip(';')
                try:
                    trains_data = json.loads(json_str)
                except json.JSONDecodeError:
                    print("Warning: Could not parse trains-data.js")
    
    # Read calendar data
    calendar_data = {}
    calendar_file = script_dir / 'calendar-data.js'
    if calendar_file.exists():
        with open(calendar_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract JSON from "window.calendarData = {...};"
            if 'window.calendarData = ' in content:
                json_str = content.replace('window.calendarData = ', '').rstrip(';')
                try:
                    calendar_data = json.loads(json_str)
                except json.JSONDecodeError:
                    print("Warning: Could not parse calendar-data.js")
    
    # Find the placeholder and replace it with embedded data
    old_placeholder = '''    <script>
        // PLACEHOLDER: Data will be embedded here by generate_static_html.py
        // This ensures simple browsers (like TRMNL) get fresh data on every visit
        window.trainsData = null;
        window.calendarData = null;
    </script>'''
    
    # New embedded script with actual data
    new_script = f'''    <script>
        // Embedded data for simple browsers (like TRMNL) that don't wait for async script loads
        window.trainsData = {json.dumps(trains_data)};
        window.calendarData = {json.dumps(calendar_data)};
        
        // Display the data immediately
        if (window.calendarData && window.calendarData.events) {{
            displayCalendarEvents(window.calendarData.events);
        }} else {{
            loadCalendarEvents();
        }}
        
        if (window.trainsData && window.trainsData.departures) {{
            fetchTrains();
        }}
    </script>'''
    
    # Replace placeholder in HTML
    html_content = html_content.replace(old_placeholder, new_script)
    
    # Write the generated HTML
    output_file = script_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated static HTML with embedded data")
    print(f"  - Trains: {len(trains_data.get('departures', []))} departures")
    print(f"  - Calendar: {len(calendar_data.get('events', []))} events")

if __name__ == '__main__':
    generate_static_html()
