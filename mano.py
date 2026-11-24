

#  Load employees.csv from Day 3 (creates a sample if not present)
csv_path = "employees.csv"
if not os.path.exists(csv_path):
    sample_data = pd.DataFrame({
        "id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],
        "department": [
            "Engineering",
            "Sales",
            "HR",
            "Engineering",
            "Sales",
            "Marketing",
            "Engineering",
            "HR",
            "Sales",
            "Marketing",
            "Engineering",
            "Sales",
        ],
        "salary": [
            75000,
            52000,
            45000,
            82000,
            58000,
            50000,
            90000,
            48000,
            61000,
            54000,
            78000,
            55000,
        ],
    })
    sample_data.to_csv(csv_path, index=False)

df = pd.read_csv(csv_path)

# Normalize column names just in case (e.g., 'Department' -> 'department')
df.columns = [col.strip().lower() for col in df.columns]

# ---------------------------------------------------------
# Chart 1: Bar chart of average salary per department
# ---------------------------------------------------------
avg_salary = df.groupby("department")["salary"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
bars = plt.bar(avg_salary.index, avg_salary.values, color="steelblue", edgecolor="black")
plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")

# Add values on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

plt.tight_layout()
plt.savefig("avg_salary_by_department.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Chart 2: Histogram of salaries with 5 bins
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.hist(df["salary"], bins=5, color="teal", edgecolor="black")
plt.title("Salary Distribution (5 Bins)")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig("salary_histogram.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Chart 3: Scatter plot of id vs salary coloured by department
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
for dept, group in df.groupby("department"):
    plt.scatter(group["id"], group["salary"], label=dept, alpha=0.8, s=60)

plt.title("Employee ID vs Salary by Department")
plt.xlabel("Employee ID")
plt.ylabel("Salary")
plt.legend(title="Department")
plt.tight_layout()
plt.savefig("id_vs_salary_scatter.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Chart 4: Line chart of monthly sales (Jan to Jun) with markers
# ---------------------------------------------------------
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 15, 14, 18, 22, 25]

plt.figure(figsize=(8, 5))
plt.plot(months, sales, marker="o", linestyle="-", color="darkorange", linewidth=2, label="Monthly Sales")
plt.title("Monthly Sales (Jan to Jun)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("monthly_sales_line.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Bonus Challenge: All 4 charts on one 2x2 figure
# ---------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Top-left: Bar chart
bars_sub = axes[0, 0].bar(avg_salary.index, avg_salary.values, color="steelblue", edgecolor="black")
axes[0, 0].set_title("Average Salary per Department")
axes[0, 0].set_xlabel("Department")
axes[0, 0].set_ylabel("Average Salary")
for bar in bars_sub:
    h = bar.get_height()
    axes[0, 0].text(bar.get_x() + bar.get_width() / 2, h, f"{h:,.0f}", ha="center", va="bottom", fontsize=8)

# Top-right: Histogram
axes[0, 1].hist(df["salary"], bins=5, color="teal", edgecolor="black")
axes[0, 1].set_title("Salary Distribution (5 Bins)")
axes[0, 1].set_xlabel("Salary")
axes[0, 1].set_ylabel("Frequency")

# Bottom-left: Scatter plot
for dept, group in df.groupby("department"):
    axes[1, 0].scatter(group["id"], group["salary"], label=dept, alpha=0.8, s=50)
axes[1, 0].set_title("ID vs Salary by Department")
axes[1, 0].set_xlabel("ID")
axes[1, 0].set_ylabel("Salary")
axes[1, 0].legend(title="Department", fontsize=8)

# Bottom-right: Line chart
axes[1, 1].plot(months, sales, marker="o", linestyle="-", color="darkorange", linewidth=2, label="Sales")
axes[1, 1].set_title("Monthly Sales (Jan to Jun)")
axes[1, 1].set_xlabel("Month")
axes[1, 1].set_ylabel("Sales")
axes[1, 1].legend()
axes[1, 1].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("all_charts_subplot.png", dpi=300)
plt.close()

print("All charts generated successfully!")
