import streamlit as st
import pandas as pd
from utils_credit import parse_credit_pdf
from utils_bank import parse_bank_pdf

st.set_page_config(page_title="רמזור דף חדש – הדרך הנכונה לצאת מהחובות", layout="wide")

st.title("🚦 רמזור דף חדש")
st.subheader("הדרך הנכונה לצאת מהחובות – העלה מסמכים וענה על מספר שאלות")

# --- קלט: שאלון רמזור ---
st.markdown("### 📝 שאלון ראשוני")
event = st.text_input("האם קרה משהו חריג שבגללו פנית?")
alt_funding = st.text_input("האם יש מקורות מימון נוספים שנבדקו?")
income = st.number_input("מה סך ההכנסות החודשיות (נטו) של שני בני הזוג?", min_value=0)
expenses = st.number_input("מה סך ההוצאות הקבועות החודשיות?", min_value=0)
other_loans = st.text_input("האם קיימות הלוואות נוספות? פרט/י והוסף/י גובה החזר חודשי")
is_balanced = st.radio("האם אתם מאוזנים כלכלית?", ["כן", "לא"])
is_likely_to_change = st.radio("האם צפוי שינוי כלשהו במצב בשנה הקרובה?", ["כן", "לא"])

st.markdown("---")

# --- העלאת קבצים ---
st.markdown("### 📤 העלאת קבצים")
credit_file = st.file_uploader("העלה את דוח נתוני האשראי (PDF)", type="pdf")
bank_file = st.file_uploader('העלה את דוח העו"ש (PDF)', type="pdf")

# --- עיבוד ---
if credit_file and bank_file and income:
    with st.spinner("📊 מעבד נתונים..."):
        credit_df, credit_summary = parse_credit_pdf(credit_file)
        bank_df, bank_summary = parse_bank_pdf(bank_file)

        # חישוב יחס חוב/הכנסה שנתי
        total_debt = credit_summary['total_debt']
        annual_income = income * 12
        debt_ratio = total_debt / annual_income if annual_income > 0 else 0

        if debt_ratio < 1:
            color = "🟢 ירוק"
        elif debt_ratio < 2:
            color = "🟡 צהוב"
        else:
            color = "🔴 אדום"

        st.success("הקבצים עובדו בהצלחה")
        st.markdown(f"### 🧾 סיכום כלכלי")
        st.write(f"**סה\"כ חוב כולל:** {total_debt:,.0f} ש\"ח")
        st.write(f"**יחס חוב להכנסה שנתית:** {debt_ratio:.2f}")
        st.write(f"**רמת סיכון לפי רמזור:** {color}")

        with st.expander("📄 פרטי דוח אשראי"):
            st.dataframe(credit_df)

        with st.expander('🏦 תנועות עו"ש'):
            st.dataframe(bank_df)

else:
    st.info("יש למלא את כל השדות ולהעלות את שני הקבצים")
