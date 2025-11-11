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
    
    # Read the base HTML template
    html_file = script_dir / 'index.html'
    with open(html_file, 'r', encoding='utf-8') as f:
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
    
    # Find the data loading script section and replace it with embedded data
    # Find the section that loads trains-data.js and calendar-data.js
    old_script = '''    <script>
        // Add cache-busting timestamp to force fresh data from GitHub Pages
        const timestamp = new Date().getTime();
        
        // Load calendar data
        const calendarScript = document.createElement('script');
        calendarScript.src = `calendar-data.js?t=${timestamp}`;
        document.head.appendChild(calendarScript);
        
        // Load train data
        const trainsScript = document.createElement('script');
        trainsScript.src = `trains-data.js?t=${timestamp}`;
        document.head.appendChild(trainsScript);
        
        // Properly wait for both scripts to load with timeout
        function waitForDataAndDisplay() {
            const maxWaitTime = 5000; // 5 second timeout
            const startTime = Date.now();
            
            function check() {
                const calendarReady = typeof window.calendarData !== 'undefined';
                const trainsReady = typeof window.trainsData !== 'undefined';
                const elapsed = Date.now() - startTime;
                
                if (calendarReady && trainsReady) {
                    // Both loaded successfully
                    displayCalendarEvents(window.calendarData.events);
                    fetchTrains();
                } else if (elapsed >= maxWaitTime) {
                    // Timeout - use fallbacks
                    if (!calendarReady) {
                        loadCalendarEvents();
                    } else {
                        displayCalendarEvents(window.calendarData.events);
                    }
                    
                    if (!trainsReady) {
                        fetchTrains(); // Will show "S-tog data not loaded" or fallback
                    } else {
                        fetchTrains();
                    }
                } else {
                    // Keep checking
                    setTimeout(check, 50);
                }
            }
            
            check();
        }
        
        waitForDataAndDisplay();
    </script>'''
    
    # New embedded script
    new_script = f'''    <script>
        // Embed data directly to support simple browsers (like TRMNL) that don't wait for async script loads
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
    
    # Replace in HTML
    html_content = html_content.replace(old_script, new_script)
    
    # Write the generated HTML
    output_file = script_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated static HTML with embedded data")
    print(f"  - Trains: {len(trains_data.get('departures', []))} departures")
    print(f"  - Calendar: {len(calendar_data.get('events', []))} events")

if __name__ == '__main__':
    generate_static_html()
