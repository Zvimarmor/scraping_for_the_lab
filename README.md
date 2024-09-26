# Gene Interaction Finder: tRFs and miRNAs

## Overview

This Python program is designed to automate the retrieval of gene interactions related to **tRFs (transfer RNA-derived fragments)** and **miRNAs (microRNAs)**. The program accesses relevant web resources, performs searches based on input data, and saves the results as CSV files. It allows users to analyze genes targeted by tRFs and miRNAs by querying external websites such as [tRFTar](http://www.rnanut.net/tRFTar/) for tRFs and [mirDIP](https://ophid.utoronto.ca/mirDIP/index.jsp#r) for miRNAs.

## Features

- **tRF Analysis**: Retrieves gene interactions for tRFs by querying the tRFTar database.
- **miRNA Analysis**: Retrieves gene interactions for miRNAs using the mirDIP tool.
- **tRF and miRNA Analysis**: Analyze both tRFs and miRNAs in combination to identify gene targets shared between them.
- **Results Export**: Option to save the results in CSV format for easy access and further analysis.

## How to Use

### Step 1: Install Dependencies
Make sure you have Python installed. To install the required packages, run:

```bash
pip install -r requirements.txt
```

### Step 2: Prepare Input Files
- **tRFs File**: A CSV file where the first column contains the list of tRFs.
- **miRNAs File**: A CSV file where the first column contains the list of miRNAs.

### Step 3: Running the Program
You can run the program from the terminal using Python. Here are the available options:

1. **Check Genes for tRFs**:
   - When prompted, enter `1`.
   - You will be asked to provide the path to your tRF CSV file.
   - The program will retrieve the genes associated with the given tRFs.

2. **Check Genes for miRNAs**:
   - When prompted, enter `2`.
   - You will be asked to provide the path to your miRNA CSV file.
   - You can specify a minimum score (default: 0.8) for filtering gene interactions.
   - The program will retrieve genes associated with the given miRNAs.

3. **Check Genes for Both tRFs and miRNAs**:
   - When prompted, enter `3`.
   - Provide paths to both the tRF and miRNA CSV files.
   - The program will analyze genes targeted by both tRFs and miRNAs and export the combined results.

### Step 4: Review Output
The program will save results in CSV format. By default:
- tRF results are saved as `conclusion_TRFs_genes.csv`.
- miRNA results are saved as `conclusion_miRNAs_genes.csv`.
- Combined results are saved as `conclusion_genes.csv`.

## Customizing Program Behavior

### 1. **Time Wait Adjustment**
The program uses time delays to ensure proper page loading when interacting with websites. The delay is controlled by the `TIME_WAIT` constant, which is set to 3 seconds by default. You can adjust it to suit your internet speed:

```python
TIME_WAIT = 5  # Adjust the delay in seconds
```

### 2. **Output Directory**
The program saves output files in the current working directory by default. You can modify the directory to your preference by changing the `prefs` in the miRNA section where download options are set:

```python
prefs = {"download.default_directory": "/your/preferred/path"}  # Set your directory here
```

---

## Requirements

Here is a list of the required Python packages to run this program. You can find these in the `requirements.txt` file:

```
pandas
numpy
selenium
webdriver-manager
```

Ensure that the Chrome browser is installed on your machine, as Selenium uses it to automate web interaction.

## Notes
- Make sure you have **Google Chrome** installed and up-to-date for Selenium to work correctly.
- You may need to adjust the `TIME_WAIT` constant depending on your network speed or the responsiveness of the target websites.

## Author

zvi Marmor, for the Soreq's Lab, ELSC
if you have any problems/bugs in the program let me know

zvi.marmor@mail.huji.ac.il

1. **Where to add your name and email**:  
   A good place to add your name and email would be at the end of the README under a **Contact** or **Author** section. It makes it clear for anyone who needs help or has questions about the project. You can also include it right after the title under an "Author" heading if you want to emphasize ownership upfront.

2. **Hebrew Translation**:  
Here’s the README content translated into Hebrew:

---

# חיפוש אינטראקציות גנים: tRFs ו-miRNAs

## סקירה כללית

התוכנית הזו ב-Python מיועדת לאוטומציה של שליפת אינטראקציות גנים הקשורות ל-**tRFs (קטעי RNA נגזרי tRNA)** ול-**miRNAs (מיקרו-RNA)**. התוכנית ניגשת לאתרים רלוונטיים, מבצעת חיפושים על פי נתונים שהוזנו ושומרת את התוצאות כקבצי CSV. התוכנית מאפשרת למשתמשים לנתח גנים המכוונים על ידי tRFs ו-miRNAs באמצעות שאילתות באתרים חיצוניים כמו [tRFTar](http://www.rnanut.net/tRFTar/) עבור tRFs ו-[mirDIP](https://ophid.utoronto.ca/mirDIP/index.jsp#r) עבור miRNAs.

## תכונות עיקריות

- **ניתוח tRFs**: שולף אינטראקציות גנים עבור tRFs על ידי שאילתת מסד הנתונים tRFTar.
- **ניתוח miRNAs**: שולף אינטראקציות גנים עבור miRNAs באמצעות הכלי mirDIP.
- **ניתוח משולב של tRFs ו-miRNAs**: ניתוח משותף לזיהוי גנים המשותפים ל-tRFs ול-miRNAs.
- **ייצוא תוצאות**: אפשרות לשמירת התוצאות בפורמט CSV לצורך גישה נוחה וניתוח נוסף.

## כיצד להשתמש

### שלב 1: התקנת תלותים
וודא ש-Python מותקן אצלך. להתקנת החבילות הנדרשות, יש להריץ:

```bash
pip install -r requirements.txt
```

### שלב 2: הכנת קבצי קלט
- **קובץ tRFs**: קובץ CSV כאשר העמודה הראשונה מכילה את רשימת ה-tRFs.
- **קובץ miRNAs**: קובץ CSV כאשר העמודה הראשונה מכילה את רשימת ה-miRNAs.

### שלב 3: הפעלת התוכנית
ניתן להפעיל את התוכנית ממסוף (terminal) באמצעות Python. הנה האפשרויות הזמינות:

1. **בדיקת גנים עבור tRFs**:
   - כשתישאל, הזן `1`.
   - תתבקש לספק את הנתיב לקובץ ה-tRF שלך.
   - התוכנית תשלוף את הגנים המשויכים ל-tRFs שסיפקת.

2. **בדיקת גנים עבור miRNAs**:
   - כשתישאל, הזן `2`.
   - תתבקש לספק את הנתיב לקובץ ה-miRNA שלך.
   - תוכל להגדיר ציון מינימלי (ברירת מחדל: 0.8) לסינון אינטראקציות גנים.
   - התוכנית תשלוף את הגנים המשויכים ל-miRNAs שסיפקת.

3. **בדיקת גנים עבור tRFs ו-miRNAs**:
   - כשתישאל, הזן `3`.
   - ספק נתיבים לשני קבצי ה-tRF וה-miRNA.
   - התוכנית תנתח את הגנים המשותפים לשני ה-RNAs ותשמור את התוצאות כקובץ CSV.

### שלב 4: בדיקת התוצאות
התוכנית תשמור את התוצאות בפורמט CSV. ברירת המחדל:
- תוצאות עבור tRFs יישמרו כ-`conclusion_TRFs_genes.csv`.
- תוצאות עבור miRNAs יישמרו כ-`conclusion_miRNAs_genes.csv`.
- תוצאות משולבות יישמרו כ-`conclusion_genes.csv`.

## התאמת פעולת התוכנית

### 1. **הגדרת זמן ההמתנה**
התוכנית משתמשת בהמתנות כדי להבטיח טעינת עמודים מלאה בעת תקשורת עם אתרים. הזמן נקבע על ידי הקבוע `TIME_WAIT`, אשר ברירת המחדל שלו היא 3 שניות. ניתן לשנות אותו לפי מהירות האינטרנט שלך:

```python
TIME_WAIT = 5  # שינוי זמן ההמתנה בשניות
```

### 2. **תיקיית שמירת קבצים**
התוכנית שומרת קבצי פלט בתיקייה הנוכחית כברירת מחדל. ניתן לשנות את התיקייה לפי הצורך על ידי שינוי ההגדרה `prefs` בחלק של miRNA בו מוגדרות אפשרויות ההורדה:

```python
prefs = {"download.default_directory": "/הנתיב/המועדף/שלך"}  # הגדרת התיקייה כאן
```

---

## דרישות

להלן רשימת החבילות הדרושות להפעלת התוכנית. תוכל למצוא את הרשימה בקובץ `requirements.txt`:

```
pandas
numpy
selenium
webdriver-manager
```

וודא כי דפדפן **Google Chrome** מותקן אצלך במחשב, מאחר ו-Selenium משתמש בו לאוטומציה של אינטראקציה עם אתרים.

## הערות
- וודא כי **Google Chrome** מותקן ומעודכן במחשב שלך כדי ש-Selenium יפעל כהלכה.
- ייתכן שתצטרך להתאים את הקבוע `TIME_WAIT` בהתאם למהירות הרשת או לתגובתיות האתרים.

---

## מחבר
התוכנית נכתבה על ידי צבי מרמור עבור מעבדת שורק, elsc
אם אתה מוצא באגים או בעיות בתוכנית, צור איתי קשר ונסבול יחד!

zvi.marmor@mail.huji.ac.il

