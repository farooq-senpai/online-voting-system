from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Party
from otp import generate_otp, send_otp, store_otp, verify_otp_logic

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'voter':
            return redirect(url_for('voting.voter_dashboard'))
        else:
            return redirect(url_for('voting.party_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Email not found. Please register.', 'error')
            return redirect(url_for('auth.login'))

        if user.role != role:
            flash(f'Invalid role selected. This email is registered as a {user.role}.', 'error')
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            flash('Incorrect password.', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.is_verified:
            # Resend OTP flow if needed, or just redirect to verify
            otp = generate_otp()
            if send_otp(email, otp):
                store_otp(email, otp)
                session['email_to_verify'] = email
                flash('Account not verified. A new OTP has been sent.', 'info')
                return redirect(url_for('auth.verify_otp'))
            else:
                flash('Error sending OTP. Please try again.', 'error')
                return redirect(url_for('auth.login'))

        login_user(user)
        if user.role == 'voter':
            return redirect(url_for('voting.voter_dashboard'))
        else:
            return redirect(url_for('voting.party_dashboard'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('voting.voter_dashboard')) # Default redirect

    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Party specific
        party_name = request.form.get('party_name')
        party_symbol = request.form.get('party_symbol') # In a real app, handle file upload

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.register'))

        if role == 'party' and Party.query.filter_by(name=party_name).first():
            flash('Party name already exists.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, full_name=full_name, role=role, is_verified=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        if role == 'party':
            new_party = Party(name=party_name, symbol=party_symbol, user_id=new_user.id)
            db.session.add(new_party)
            db.session.commit()

        # Send OTP
        otp = generate_otp()
        if send_otp(email, otp):
            store_otp(email, otp)
            session['email_to_verify'] = email
            flash('Registration successful! Please verify your email.', 'success')
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Error sending OTP. Registration complete but verification failed. Login to retry.', 'warning')
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('email_to_verify')
    if not email:
        flash('Session expired or invalid access.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        otp_input = request.form.get('otp')
        if verify_otp_logic(email, otp_input):
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                db.session.commit()
                session.pop('email_to_verify', None)
                flash('Account verified! You can now login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('User not found.', 'error')
        else:
            flash('Invalid OTP. Please try again.', 'error')

    return render_template('otp_verify.html', email=email)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
