@echo off

echo מחיקת ריפו קודם (אם קיים)...
rmdir /s /q .git

echo אתחול Git חדש...
git init

echo הגדרת שם משתמש ואימייל...
git config user.name "lia"
git config user.email "ttrwlyh@example.com"

echo הוספת כל הקבצים...
git add .

echo ביצוע קומיט ראשון...
git commit -m "first commit"

echo שינוי שם הסניף ל-main...
git branch -M main

echo חיבור לריפו מרוחק בגיטהאב...
git remote add origin https://github.com/liatetro/discord-counting-bott.git

echo העלאה לגיטהאב...
git push -u origin main

pause



