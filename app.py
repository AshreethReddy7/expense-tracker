from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# PostgreSQL Connection
def get_connection():
    return psycopg2.connect(
        host="ep-winter-water-aordh8gr-pooler.c-2.ap-southeast-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_lEbSZ2mFCk5P",
        port=5432,
        sslmode = 'require'
    )
app = Flask(__name__)


# =========================
# HOME PAGE - ACCOUNT FORM
# =========================
@app.route('/')
def home():
    return render_template('form.html')


# =========================
# SAVE ACCOUNT
# =========================
@app.route('/submit_account', methods=['POST'])
def submit_account():
    conn = get_connection()
    cur = conn.cursor()

    try:

        account_code = request.form['account_code']
        account_name = request.form['account_name']
        pl_bs = request.form['pl_bs']
        account_group = request.form['account_group']
        account_sub_group = request.form['account_sub_group']
        account_type = request.form['account_type']
        gst_number = request.form['gst_number']
        pan_number = request.form['pan_number']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin = request.form['pin']
        country = request.form['country']
        email = request.form['email']
        phone = request.form['phone']

        query = """
        INSERT INTO accounts (
            account_code,
            account_name,
            pl_bs,
            account_group,
            account_sub_group,
            account_type,
            gst_number,
            pan_number,
            address,
            city,
            state,
            pin,
            country,
            email,
            phone
        )

        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )

        ON CONFLICT (account_code)
        DO NOTHING
        """

        values = (
            account_code,
            account_name,
            pl_bs,
            account_group,
            account_sub_group,
            account_type,
            gst_number,
            pan_number,
            address,
            city,
            state,
            pin,
            country,
            email,
            phone
        )

        cur.execute(query, values)

        conn.commit()

        # Redirect to transaction form
        return redirect(url_for(
            'transaction_form',
            account_code=account_code,
            account_name=account_name
        ))

    except Exception as e:

        conn.rollback()

        return f"Database Error: {str(e)}"
    finally:
        cur.close()
        conn.close()

# =========================
# TRANSACTION FORM PAGE
# =========================
@app.route('/transaction')
def transaction_form():

    account_code = request.args.get('account_code')
    account_name = request.args.get('account_name')

    return render_template(
        'transaction.html',
        account_code=account_code,
        account_name=account_name
    )


# =========================
# SAVE TRANSACTION
# =========================
@app.route('/save_transaction', methods=['POST'])
def save_transaction():
    conn = get_connection()
    cur = conn.cursor()

    try:

        account_code = request.form['account_code']
        account_name = request.form['account_name']
        transaction_date = request.form['transaction_date']
        transaction_type = request.form['transaction_type']
        amount = request.form['amount']
        remarks = request.form['remarks']

        query = """
        INSERT INTO transactions (
            account_code,
            account_name,
            transaction_date,
            transaction_type,
            amount,
            remarks
        )

        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            account_code,
            account_name,
            transaction_date,
            transaction_type,
            amount,
            remarks
        )

        cur.execute(query, values)

        conn.commit()

        return redirect(url_for('transaction_report'))

    except Exception as e:

        conn.rollback()

        return f"Database Error: {str(e)}"
    finally:
        cur.close()
        conn.close()


# =========================
# TRANSACTION REPORT
# =========================
@app.route('/report')

def transaction_report():

    conn = get_connection()

    cur = conn.cursor()

    query = """

    SELECT
        transaction_id,
        account_code,
        account_name,
        transaction_date,
        transaction_type,
        amount,
        remarks

    FROM transactions

    ORDER BY transaction_id DESC

    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('report.html', data=data)
if __name__ == '__main__':
    app.run(debug=False)