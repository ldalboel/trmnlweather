#!/usr/bin/env python3
"""
Fetch departures from Danshøj station and save to JSON.
Uses the Rejseplanen web interface with two different URLs.
Fetches up to 8 departures, using prognosis time if available.
"""

import json
import re
from datetime import datetime, timedelta

def fetch_train_departures():
    """Fetch next 8 departures from both trains and buses, combining results."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Build URLs with current date and time plus 5 minutes (handles day roll-over)
        target_dt = datetime.now() + timedelta(minutes=5)
        today = target_dt.strftime('%d.%m.%Y')
        current_time = target_dt.strftime('%H:%M')
        
        # URL 1: Trains from Danshøj
        url1 = f'https://webapp.rejseplanen.dk/bin/stboard.exe/mn?L=vs_rp4.vs_dsb&ml=m&L=vs_rp4.vs_dsb&protocol=https:&ml=m&boardType=dep&input=Dansh%F8j%20St.%238600742&dirInput=K%F8benhavn%20H%238600626&productsFilter=111111111111&maxStops=0&maxJourneys=7&selectDate=period&dateBegin={today}&dateEnd={today}&time={current_time}&currentSqResultsContentType=STATIONBOARD&start=yes&'
        
        # URL 2: Buses from Maribovej
        url2 = f'https://webapp.rejseplanen.dk/bin/stboard.exe/mn?L=vs_rp4.vs_dsb&ml=m&L=vs_rp4.vs_dsb&protocol=https:&ml=m&boardType=dep&input=Maribovej%20(Vigerslevvej)%237157&productsFilter=111111111111&maxStops=0&maxJourneys=7&selectDate=period&dateBegin={today}&dateEnd={today}&time={current_time}&currentSqResultsContentType=STATIONBOARD&start=yes&'
        
        urls_to_try = [
            (url1, "Trains (Danshøj St.)"),
            (url2, "Buses (Maribovej)")
        ]
        
        departures = []
        
        for url, url_type in urls_to_try:
            try:
                print(f"Fetching {url_type}...")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all departure rows with sqToggleDetails class
                rows = soup.find_all('tr', class_=lambda x: x and 'sqToggleDetails' in x)
                
                print(f"  Found {len(rows)} departure rows")
                
                for row in rows:
                    try:
                        cells = row.find_all('td')
                        if len(cells) < 4:
                            continue
                        
                        # Cell 0 (sqFirst): scheduled time
                        time_str = cells[0].get_text(strip=True)
                        if ':' not in time_str:
                            continue
                        
                        # Cell 1: prognosis time (may be empty)
                        prognosis_time = None
                        if len(cells) > 1:
                            prognosis_text = cells[1].get_text(strip=True)
                            # Look for time in format "ca. HH:MM" or just "HH:MM"
                            time_match = re.search(r'(\d{1,2}:\d{2})', prognosis_text)
                            if time_match:
                                prognosis_time = time_match.group(1)
                        
                        # Use prognosis time if available, otherwise scheduled time
                        display_time = prognosis_time if prognosis_time else time_str
                        
                        # Cell 2 (sqProd): line/product
                        line_cell_text = cells[2].get_text(strip=True)
                        
                        # For buses: extract just the number (e.g., "Bus    10" -> "10")
                        # For trains: extract the letter (e.g., "B" -> "B")
                        bus_match = re.search(r'Bus\s+(\d+)', line_cell_text)
                        if bus_match:
                            line = bus_match.group(1)  # Extract number for buses
                        else:
                            # For trains, extract letter(s)
                            train_match = re.search(r'^([A-H]x?)', line_cell_text)
                            if train_match:
                                line = train_match.group(1)
                            else:
                                continue
                        
                        # Determine destination based on number of cells
                        # Trains have 6 cells, buses have 4 cells
                        destination = 'Unknown'
                        if len(cells) >= 6:
                            # Train format: destination is in cell 5 (sqResultsTerminal)
                            destination_text = cells[5].get_text(strip=True)
                        elif len(cells) >= 4:
                            # Bus format: destination is in cell 3 (sqResultsTerminal)
                            destination_text = cells[3].get_text(strip=True)
                        
                        # Extract the first part before "Se alle stop" or similar
                        destination = destination_text.split('-')[0].strip()
                        
                        # Skip if no valid destination
                        if not destination or destination in ['Unknown', 'Kl', 'Afg']:
                            continue
                        
                        departures.append({
                            'time': display_time,
                            'destination': destination,
                            'line': line,
                            'is_realtime': prognosis_time is not None,
                            'url_source': url_type
                        })
                        
                    except Exception as e:
                        continue
                    
            except Exception as e:
                print(f"  ✗ {url_type} failed: {e}")
                continue
        
        # Sort departures by time and take the first 8
        if departures:
            # Parse times for sorting (HH:MM format)
            def parse_time(departure):
                try:
                    hours, minutes = map(int, departure['time'].split(':'))
                    return hours * 60 + minutes
                except:
                    return 9999
            
            departures.sort(key=parse_time)
            departures = departures[:8]
            
            print(f"\n✓ Combined results from both sources")
            print(f"✓ Showing {len(departures)} nearest departures:")
            for dep in departures:
                realtime_indicator = " (realtime)" if dep['is_realtime'] else ""
                print(f"  - {dep['time']}: Line {dep['line']} → {dep['destination']} [{dep['url_source']}]{realtime_indicator}")
            return departures
        
        # If we got here, both URLs failed
        raise Exception("Both URLs failed to fetch departures")
        
    except Exception as e:
        print(f"✗ Error fetching trains from Rejseplanen: {e}")
        print("  Using fallback mock data")
        
        # Fallback: Use mock data
        now = datetime.now()
        mock_departures = [
            {
                'time': (now + timedelta(minutes=7)).strftime('%H:%M'),
                'destination': 'Ryparken St.',
                'line': 'F',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=12)).strftime('%H:%M'),
                'destination': 'Farum St.',
                'line': 'B',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=18)).strftime('%H:%M'),
                'destination': 'København Syd St.',
                'line': 'F',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=25)).strftime('%H:%M'),
                'destination': 'Høje Taastrup St.',
                'line': 'B',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=32)).strftime('%H:%M'),
                'destination': 'Køge St.',
                'line': 'E',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=37)).strftime('%H:%M'),
                'destination': 'Ballerup St.',
                'line': 'A',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=42)).strftime('%H:%M'),
                'destination': 'Lyngby St.',
                'line': 'C',
                'is_realtime': False
            },
            {
                'time': (now + timedelta(minutes=48)).strftime('%H:%M'),
                'destination': 'Hillerød St.',
                'line': 'H',
                'is_realtime': False
            }
        ]
        print(f"  Using {len(mock_departures)} mock departures")
        return mock_departures

if __name__ == '__main__':
    departures = fetch_train_departures()
    
    # Save to trains-data.js
    train_data = {
        'updated': datetime.now().isoformat(),
        'station': 'Danshøj / Maribovej',
        'departures': departures
    }
    
    with open('trains-data.js', 'w') as f:
        f.write('window.trainsData = ')
        f.write(json.dumps(train_data))
        f.write(';')
    
    print(f"✓ Saved train data to trains-data.js")

