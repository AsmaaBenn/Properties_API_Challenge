# Properties_API_Challenge
<p>
In this Code, i develop an asynchronously API with FastAPI and MongoDB.<br/>
I'll be using the Motor package to interact with MongoDB asynchronously.
</p>
<p>
  <h3>Initial Setup</h3>
  Start by creating and activate a virtual environment. <br/><br/>
  Next, Install the dependencies in requirements.txt file <br/>
  <pre><code> pip install -r requirements.txt</code></pre>
  
  In the challenge/main.py file, there is an entry point for running the application
</p>
<p>
  <h3>MongoDB</h3>
  We need to wire up MongoDB and configure our application to communicate with it.<br/>
  <h4>MongoDB Setup</h4>
  <lu>
  <li>installe MongoDB on your machine, refer to the 
    [installation guide](https://docs.mongodb.com/manual/installation/).</li>
  <li>run the mongod daemon process.</li>
  <pre><code>mongod --dbpath ~/data/db/</code></pre>
  </lu>
</p>
