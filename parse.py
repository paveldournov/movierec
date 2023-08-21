import csv
from datetime import date
from bs4 import BeautifulSoup

# Parse HTML 
with open('netflix.html', encoding='utf-8') as f:
  soup = BeautifulSoup(f, 'html.parser')

# Extract data
ratings = []

li_lines = soup.find_all("li")
my_rows = list(filter(lambda l: l.get("class") == ['retableRow'], li_lines))

for r in my_rows:
    dd = r.find_all("div")
    if len(dd) > 2 and ("date" in dd[0].get("class")):
        r_date = dd[0].text
        r_title = dd[1].text
        r_rating = dd[2]

        r_rating_num = -1

        bb = r_rating.find_all("button")
        if len(bb) > 0:
            # new thumbs up/down system
            for b in bb:
                button_label = b.get("arialabel")
                if button_label == "Already rated: thumbs up (click to remove rating)":
                    r_rating_num = 4
                    break                
                elif button_label == "Already rated: thumbs down (click to remove rating)":
                    r_rating_num = 1
                    break
                elif button_label == "Already rated: two thumbs up (click to remove rating)":
                    r_rating_num = 5
                    break
        else:
            # old star system
            bb = r_rating.find_all("span")
            if len(bb) > 0:
               r_rating_num = 0
               for s in bb:
                   if "personal" in s.get("class"):
                       star_num = int(s.get("data-rating"))
                       if star_num > r_rating_num:
                           r_rating_num = star_num
                           

        ratings.append([r_date, r_title, r_rating_num]) 


# Write CSV
with open('netflix1.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['date', 'title', 'rating'])
  for r in ratings:
    writer.writerow(r)

