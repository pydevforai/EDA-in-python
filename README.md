# Sales Data Analysis — Practice Project

A end-to-end data analysis project on a raw, messy sales dataset covering 20 orders across multiple regions, salespersons, and product categories in Pakistan. The goal was to clean the data, engineer new columns, answer real business questions, and think critically about what the data actually means.

---

## Dataset Overview

| Column | Description |
|--------|-------------|
| Order_ID | Unique order identifier |
| Salesperson | Name of the salesperson who made the sale |
| Region | City where the order was placed (Karachi, Lahore, Islamabad) |
| Category | Product category (Electronics, Clothing, Furniture) |
| Units_Sold | Number of units sold per order |
| Unit_Price | Price per unit in PKR |
| Discount_% | Discount applied on the order |
| Month | Month the order was placed (Jan–Jun) |
| Returned | Whether the order was returned (Yes/No) |

**Raw issues in the data:** missing values in Salesperson and Units_Sold columns, no revenue columns, discount stored as integer percentage, Returned stored as Yes/No strings.

---

## Tools Used

- Python
- Pandas
- NumPy
- Seaborn
- Jupyter Notebook

---

## What I Did

### Section 1 — Data Inspection
- Loaded the dataset from a CSV file to simulate a real workflow
- Checked shape, datatypes, and full info summary
- Identified null values per column
- Checked for duplicate rows
- Dropped the extra index column created during CSV export

### Section 2 — Data Cleaning
- **Salesperson nulls** — filled with mode because it is a categorical column and the dataset is small. Mode represents the most frequently occurring salesperson, which is the best available guess for a categorical field.
- **Units_Sold nulls** — checked for outliers first using a Seaborn boxplot. Found no outliers, so filled with mean. Mean is appropriate here because without outliers the average accurately represents the center of the data.
- **Created Total_Revenue** — calculated as Units_Sold × Unit_Price
- **Created Final_Revenue** — converted Discount_% to decimal first, calculated discount amount, then subtracted from Total_Revenue
- **Converted Returned column** — replaced Yes/No with 1/0 integers to enable numerical aggregation in groupby operations

### Section 3 — Business Questions
Answered five business questions using groupby:
- Which salesperson generated the highest total revenue?
- Which region sold the most units?
- Which product category has the highest average price?
- Which month had the highest total revenue?
- How many orders were returned per region?

### Section 4 — Filtering
- Orders from Karachi in the Electronics category
- Orders with discount greater than 10%
- Orders where Units_Sold > 20 AND Final_Revenue > 100,000

### Section 5 — Business Thinking
Answered three open-ended thinking questions as comments:
- Explained why mean was chosen over median for Units_Sold
- Analyzed what a high return rate in Karachi tells us about the business
- Gave a full management recommendation for a salesperson with high revenue but also high returns — covering net revenue analysis, sales tactics review, and post-sale support

---

## Key Decisions Made

**Why mode for Salesperson?**
Salesperson is a categorical variable. You cannot calculate a mean or median for names. Mode gives the most frequently occurring value which is the most reasonable fill for a small dataset.

**Why mean for Units_Sold?**
Before filling, I verified there were no outliers using a boxplot. With no outliers present, the mean is a fair representation of the average units sold and will not distort the distribution.

**Why convert Returned to 0 and 1?**
Storing Yes/No as integers allows direct use of groupby + sum to count total returns per group — clean and efficient without needing extra filtering logic.

---

## Business Insights Found

- Karachi had the highest return rate among all regions, suggesting possible issues with customer targeting, product quality, or salesperson practices in that region
- A salesperson with high total revenue but high returns is not necessarily a top performer — net revenue after returns tells the real story
- Discount rates above 10% did not always correlate with high units sold, suggesting discounts alone do not drive volume in this dataset

---

## How to Run

1. Clone this repository
2. Open `SalesData-practice.ipynb` in Jupyter Notebook
3. Run all cells from top to bottom
4. The notebook will generate `SalesData.csv` and `Clean_SalesData.csv` automatically

---

## Author

Aspiring Data Analyst learning Python, Pandas, NumPy, and Matplotlib.  
Currently building projects to develop real analytical skills.  
GitHub: [pydevforai](https://github.com/pydevforai)
