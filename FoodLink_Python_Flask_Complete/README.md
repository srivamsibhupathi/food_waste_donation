# FoodLink - Python Flask Edition

## Run
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Open Terminal.
4. Run:
   `python -m pip install -r requirements.txt`
5. Run:
   `python app.py`
6. Open `http://127.0.0.1:5000`

If `pip` is not recognized, use `python -m pip` as shown above.

## Demo accounts
- Donor: donor@foodlink.demo / donor123
- NGO: ngo@foodlink.demo / ngo123
- Volunteer: volunteer@foodlink.demo / volunteer123
- Admin: admin@foodlink.demo / admin123

## Main features
Responsive FoodLink UI, donation form, image upload, Local JSON persistence, search/filter marketplace, matching scores, role dashboards, status workflow, notifications, ratings, charts, impact page, map-style concept and clean reusable templates.

## Data
`foodlink_data.json` is generated automatically on first run. It is the demo persistence layer. Replace this layer with Firebase/Supabase later without changing the overall page structure.

## Background image
The CSS currently uses an illustration-style hero area. To add your own background image, place it in `static/images/hero.jpg` and add:
`.hero-art{background-image:url("../images/hero.jpg");background-size:cover;background-position:center}`
to `static/css/style.css`.
