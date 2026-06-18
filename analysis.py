"""
Sleep Health and Lifestyle - Full Analysis Pipeline
Generates cleaned dataset, summary stats, correlation table, and all charts.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE = "viridis"

# ----------------------------------------------------------------
# 1. LOAD
# ----------------------------------------------------------------
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
print("Raw shape:", df.shape)

# ----------------------------------------------------------------
# 2. CLEANING
# ----------------------------------------------------------------
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('No Disorder')

# b) BMI Category
df['BMI Category'] = df['BMI Category'].replace({'Normal Weight': 'Normal'})

# c) Split Blood Pressure into Systolic / Diastolic numeric columns
bp_split = df['Blood Pressure'].str.split('/', expand=True)
df['Systolic_BP'] = bp_split[0].astype(int)
df['Diastolic_BP'] = bp_split[1].astype(int)

# d) Check duplicates (excluding Person ID)
dup_count = df.duplicated(subset=[c for c in df.columns if c != 'Person ID']).sum()
print(f"Rows sharing identical lifestyle/health profile (excl. ID): {dup_count} -- kept, as each Person ID is a distinct individual")

# e) Check for missing values after cleaning
print("\nMissing values after cleaning:\n", df.isnull().sum().sum(), "total")

# f) Data types check
df['Person ID'] = df['Person ID'].astype(int)

# Save cleaned dataset
df.to_csv('cleaned_sleep_data.csv', index=False)
print("\nCleaned dataset saved. Final shape:", df.shape)

# ----------------------------------------------------------------
# 3. DESCRIPTIVE STATISTICS
# ----------------------------------------------------------------
numeric_cols = ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level',
                 'Stress Level', 'Heart Rate', 'Daily Steps', 'Systolic_BP', 'Diastolic_BP']

desc = df[numeric_cols].describe().T
desc.to_csv('summary_statistics.csv')
print("\n--- Summary Statistics ---")
print(desc[['mean', 'std', 'min', 'max']].round(2))

print("\n--- Gender split ---")
print(df['Gender'].value_counts())

print("\n--- BMI Category split ---")
print(df['BMI Category'].value_counts())

print("\n--- Sleep Disorder split ---")
print(df['Sleep Disorder'].value_counts())

print("\n--- Avg Quality of Sleep by Occupation ---")
print(df.groupby('Occupation')['Quality of Sleep'].mean().sort_values(ascending=False).round(2))

# ----------------------------------------------------------------
# 4. CORRELATION ANALYSIS  
# ----------------------------------------------------------------
corr_cols = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level',
             'Stress Level', 'Heart Rate', 'Daily Steps', 'Systolic_BP', 'Diastolic_BP', 'Age']
corr_matrix = df[corr_cols].corr(method='pearson').round(2)
corr_matrix.to_csv('correlation_matrix.csv')
print("\n--- Correlation with Quality of Sleep ---")
print(corr_matrix['Quality of Sleep'].sort_values(ascending=False))

# ----------------------------------------------------------------
# 5. CHARTS
# ----------------------------------------------------------------
import os
FIG = 'figures/'
os.makedirs(FIG, exist_ok=True)

# Chart 1: Distribution of Sleep Duration & Quality of Sleep
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(df['Sleep Duration'], kde=True, color='#4C72B0', ax=axes[0])
axes[0].set_title('Distribution of Sleep Duration')
axes[0].set_xlabel('Sleep Duration (hours)')
sns.histplot(df['Quality of Sleep'], kde=True, color='#55A868', ax=axes[1], discrete=True)
axes[1].set_title('Distribution of Quality of Sleep')
axes[1].set_xlabel('Quality of Sleep (scale 1-10)')
plt.tight_layout()
plt.savefig(FIG + '01_distributions.png', dpi=150)
plt.close()

# Chart 2: Sleep Quality vs Stress Level
plt.figure(figsize=(7, 5.5))
sns.boxplot(data=df, x='Stress Level', y='Quality of Sleep', hue='Stress Level',
            palette=PALETTE, legend=False)
plt.title('Quality of Sleep vs Stress Level')
plt.tight_layout()
plt.savefig(FIG + '02_quality_vs_stress.png', dpi=150)
plt.close()

# Chart 3: Sleep Quality vs Physical Activity Level
plt.figure(figsize=(7, 5.5))
sns.scatterplot(data=df, x='Physical Activity Level', y='Quality of Sleep',
                 hue='Stress Level', palette=PALETTE, s=60, alpha=0.8)
plt.title('Quality of Sleep vs Physical Activity Level')
plt.tight_layout()
plt.savefig(FIG + '03_quality_vs_activity.png', dpi=150)
plt.close()

# Chart 4: Sleep Duration vs Daily Steps
plt.figure(figsize=(7, 5.5))
sns.regplot(data=df, x='Daily Steps', y='Sleep Duration',
            scatter_kws={'alpha': 0.5, 'color': '#4C72B0'}, line_kws={'color': 'red'})
plt.title('Sleep Duration vs Daily Steps')
plt.tight_layout()
plt.savefig(FIG + '04_duration_vs_steps.png', dpi=150)
plt.close()

# Chart 5: Avg Sleep Quality by Occupation
plt.figure(figsize=(9, 6))
occ_order = df.groupby('Occupation')['Quality of Sleep'].mean().sort_values(ascending=False).index
sns.barplot(data=df, y='Occupation', x='Quality of Sleep', order=occ_order,
            hue='Occupation', palette=PALETTE, legend=False, errorbar=None)
plt.title('Average Quality of Sleep by Occupation')
plt.tight_layout()
plt.savefig(FIG + '05_quality_by_occupation.png', dpi=150)
plt.close()

# Chart 6: Sleep Quality by BMI Category
plt.figure(figsize=(7, 5.5))
sns.boxplot(data=df, x='BMI Category', y='Quality of Sleep', hue='BMI Category',
            palette=PALETTE, legend=False,
            order=['Normal', 'Overweight', 'Obese'])
plt.title('Quality of Sleep by BMI Category')
plt.tight_layout()
plt.savefig(FIG + '06_quality_by_bmi.png', dpi=150)
plt.close()

# Chart 7: Correlation Heatmap
plt.figure(figsize=(8, 6.5))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap of Sleep & Lifestyle Variables')
plt.tight_layout()
plt.savefig(FIG + '07_correlation_heatmap.png', dpi=150)
plt.close()

# Chart 8: Sleep Disorder prevalence by BMI Category (stacked %)
ct = pd.crosstab(df['BMI Category'], df['Sleep Disorder'], normalize='index') * 100
ct = ct.reindex(['Normal', 'Overweight', 'Obese'])
plt.figure(figsize=(7.5, 5.5))
ct.plot(kind='bar', stacked=True, colormap=PALETTE, ax=plt.gca())
plt.title('Sleep Disorder Prevalence (%) by BMI Category')
plt.ylabel('Percentage of Group')
plt.legend(title='Sleep Disorder', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig(FIG + '08_disorder_by_bmi.png', dpi=150)
plt.close()

# Chart 9: Gender distribution & Sleep Disorder distribution (pie charts)
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axes[0],
                                   colors=['#4C72B0', '#DD8452'])
axes[0].set_ylabel('')
axes[0].set_title('Gender Distribution')
df['Sleep Disorder'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axes[1],
                                           colors=['#55A868', '#C44E52', '#8172B2'])
axes[1].set_ylabel('')
axes[1].set_title('Sleep Disorder Distribution')
plt.tight_layout()
plt.savefig(FIG + '09_gender_disorder_pie.png', dpi=150)
plt.close()

print("\nAll 9 charts saved to figures/")

# ----------------------------------------------------------------
# 6. ADDITIONAL CHARTS (10–13)
# ----------------------------------------------------------------

# Chart 10: Average Sleep Duration by Sleep Disorder
plt.figure(figsize=(7, 5.5))
disorder_order = df.groupby('Sleep Disorder')['Sleep Duration'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Sleep Disorder', y='Sleep Duration', order=disorder_order,
            hue='Sleep Disorder', palette=PALETTE, legend=False, errorbar='sd')
plt.title('Average Sleep Duration by Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Sleep Duration (hours)')
plt.tight_layout()
plt.savefig(FIG + '10_duration_by_disorder.png', dpi=150)
plt.close()

# Chart 11: Age Distribution by Sleep Disorder (violin plot)
plt.figure(figsize=(8, 5.5))
sns.violinplot(data=df, x='Sleep Disorder', y='Age',
               hue='Sleep Disorder', palette=PALETTE, legend=False,
               order=['No Disorder', 'Insomnia', 'Sleep Apnea'],
               inner='quartile')
plt.title('Age Distribution by Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Age')
plt.tight_layout()
plt.savefig(FIG + '11_age_by_disorder.png', dpi=150)
plt.close()

# Chart 12: Sleep Quality by Gender and Sleep Disorder (grouped bar)
plt.figure(figsize=(9, 5.5))
sns.barplot(data=df, x='Sleep Disorder', y='Quality of Sleep', hue='Gender',
            order=['No Disorder', 'Insomnia', 'Sleep Apnea'],
            palette=['#4C72B0', '#DD8452'], errorbar=None)
plt.title('Sleep Quality by Gender and Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Average Quality of Sleep')
plt.legend(title='Gender')
plt.tight_layout()
plt.savefig(FIG + '12_quality_gender_disorder.png', dpi=150)
plt.close()

# Chart 13: Heart Rate vs Stress Level (scatter with regression)
plt.figure(figsize=(7, 5.5))
sns.regplot(data=df, x='Stress Level', y='Heart Rate',
            scatter_kws={'alpha': 0.5, 'color': '#C44E52'},
            line_kws={'color': 'darkred'})
plt.title('Heart Rate vs Stress Level')
plt.xlabel('Stress Level')
plt.ylabel('Heart Rate (bpm)')
plt.tight_layout()
plt.savefig(FIG + '13_heartrate_vs_stress.png', dpi=150)
plt.close()

print("4 additional charts (10–13) saved to figures/")
print("\nDONE.")
