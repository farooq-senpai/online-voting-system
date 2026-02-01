from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Party, Vote

voting = Blueprint('voting', __name__)

@voting.route('/voter/dashboard')
@login_required
def voter_dashboard():
    if current_user.role != 'voter':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('voting.party_dashboard'))
    
    if current_user.has_voted:
        # Redirect to results or confirmation? User says "Redirected to confirmation/results page"
        # Let's show a "You have voted" state on the dashboard or separate page.
        # For now, let's keep them on dashboard but show different UI or redirect.
        # Requirement: "User redirected to confirmation/results page"
        return redirect(url_for('voting.vote_confirmation'))

    parties = Party.query.all()
    # "Minimum 8 political parties must exist" - We can display empty slots if < 8 or just show what we have.
    # The requirement is likely for setup, not display logic hiding < 8.
    
    return render_template('voter_dashboard.html', parties=parties, user=current_user)

@voting.route('/vote/<int:party_id>', methods=['POST'])
@login_required
def vote(party_id):
    if current_user.role != 'voter':
        flash('Only voters can vote.', 'error')
        return redirect(url_for('auth.login'))

    if current_user.has_voted:
        flash('You have already voted.', 'error')
        return redirect(url_for('voting.vote_confirmation'))

    party = Party.query.get_or_404(party_id)
    
    # Atomic vote
    new_vote = Vote(voter_id=current_user.id, party_id=party.id)
    current_user.has_voted = True
    
    db.session.add(new_vote)
    db.session.commit()
    
    flash(f'Successfully voted for {party.name}!', 'success')
    return redirect(url_for('voting.vote_confirmation'))

@voting.route('/voter/confirmation')
@login_required
def vote_confirmation():
    if not current_user.has_voted:
        return redirect(url_for('voting.voter_dashboard'))
    
    # Requirement: "See confirmation after voting".
    # User might also want to see results? "User redirected to confirmation/results page"
    # Usually real elections don't show real-time results to voters to avoid bias. 
    # But for this system, maybe? Let's stick to confirmation page.
    # Actually, Party Dashboard gets results. Voter gets confirmation.
    
    return render_template('vote_confirmation.html')

@voting.route('/party/dashboard')
@login_required
def party_dashboard():
    if current_user.role != 'party':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('voting.voter_dashboard'))
    
    # "Total votes received by: That party, Other parties (read-only)"
    my_party = current_user.party_details
    if not my_party:
        flash('Party details not found for this user.', 'error')
        return redirect(url_for('auth.login'))

    all_parties = Party.query.all()
    
    return render_template('party_dashboard.html', my_party=my_party, all_parties=all_parties)
