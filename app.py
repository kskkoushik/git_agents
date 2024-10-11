from flask import Flask, render_template, request, redirect, url_for , session , g
from github import Auth
from github import Github
from github import GithubIntegration
from ai_summarizer import ai_pullrequest_summarizer



def get_git_inst():

    if 'token' in session:
        if not hasattr(g, 'github'):
            auth = Auth.Token(session['token'])
            g.github = Github(auth=auth)
            g.github.get_user().login
        return g.github
    return None



app = Flask(__name__)

app.secret_key = "secret"

# Home page to enter GitHub access token
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token = request.form['github_token']
        session['token'] = token
        gitting = get_git_inst()
        return redirect(url_for('repos'))
    return render_template('index.html')

# Repositories page showing list of repos
@app.route('/repos')
def repos():
    # Logic to fetch repos using token will be added here
    user = get_git_inst()
    repos = user.get_user().get_repos() # Sample data for now
    return render_template('repos.html', repos=repos)

# Pull requests page for a specific repository
@app.route('/pulls/<repo>')
def pulls(repo):
    # Logic to fetch pulls using token and repo name will be added here
    pulls = repo.get_pulls() # Sample data for now
    return render_template('pulls.html', repo=repo, pulls=pulls)

@app.route('/pulls/<username>/<repo>')
def pulls_2(username , repo):
    # Logic to fetch pulls using token and repo name will be added here
    user = get_git_inst()
    repo = user.get_repo(f"{username}/{repo}") # Sample data for now
    pulls = repo.get_pulls() # Sample data for now
    return render_template('pulls.html', repo=repo.full_name, pulls= pulls)

@app.route('/summary/<title>/<body>')
def summarize(title , body):

    summary = ai_pullrequest_summarizer(title, body)
    return render_template('summary.html', summary=summary)



if __name__ == '__main__':
    app.run(debug=True)
