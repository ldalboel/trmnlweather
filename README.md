# Copenhagen Weather - TRMNL Page

A minimalist weather widget for Copenhagen optimized for TRMNL eink displays (half-page, right side).

## Features

- **Today's Weather**: Current temperature, condition, and "feels like" temperature
- **Precipitation**: Current chance of precipitation and amount
- **Next 3 Days**: Forecast with high/low temps and precipitation probability
- **Open Source**: Uses Open-Meteo API (no API key required)
- **Eink Optimized**: Black and white, ultra-thin design
- **TRMNL Half-Page**: Optimized for right-side half-page display

## Usage

### Local Testing
Simply open `index.html` in a web browser to test the weather display.

```bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000
```

### TRMNL Integration

1. Deploy `index.html` to a public URL or your local server
2. In TRMNL settings, add this URL to your custom page
3. Set the rotation to match your display orientation
4. The page will auto-refresh every 30 minutes

## API

Uses [Open-Meteo](https://open-meteo.com/) - a free, open-source weather API:
- No API key required
- No rate limiting for reasonable use
- WMO weather codes for accurate conditions
- Timezone-aware data

## Customization

### Change Location
Edit line 228-229:
```javascript
const COPENHAGEN_LAT = 55.6761;
const COPENHAGEN_LON = 12.5883;
```

To get coordinates for any city:
- Visit [Nominatim](https://nominatim.org/) or [Google Maps](https://maps.google.com/)
- Search for your city
- Note the latitude and longitude

### Adjust Refresh Rate
Edit line 251:
```javascript
setInterval(fetchWeather, 30 * 60 * 1000); // Change 30 to desired minutes
```

### Modify Styling
All CSS is at the top of the file. Key customizations:
- Font sizes in `.row-title`, `.temp`, etc.
- Colors (currently pure black/white)
- Spacing with `gap` and `padding` values
- Border styles in `.row` and `.forecast-day`

## Browser Compatibility

Works in all modern browsers. For TRMNL, ensure your device supports HTML5 and modern JavaScript.

## Deployment

### GitHub Pages (Recommended - Free)

1. **Create a GitHub repository**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/trmnlweather.git
   git branch -M main
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Under "Build and deployment" set:
     - Source: GitHub Actions
   - The deploy workflow will run automatically

3. **Access your page**
   - Your page will be live at: `https://YOUR_USERNAME.github.io/trmnlweather/`
   - Or with custom domain (Settings → Pages → Custom domain)

4. **Auto-deployment**
   - Any push to `main` or `master` branch automatically deploys
   - Workflow file: `.github/workflows/deploy.yml`

### Other Hosting Options

See README section "Where can this be hosted" for Netlify, Vercel, and self-hosted options.

## License

MIT - Use freely for personal projects

## Notes

- Weather updates every 30 minutes to respect API limits
- Displays local Copenhagen time (Europe/Copenhagen timezone)
- All values in metric (°C, mm, km/h)
- Designed for 400x480px half-page display (TRMNL standard)
- Auto-deploys to GitHub Pages on git push
