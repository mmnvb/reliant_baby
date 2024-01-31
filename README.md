<div align="center">
  <h1>👩‍🚀My Telegram assistant</h1>
  <img src="https://github.com/mmnvb/mmnvb/blob/main/img/reliant.jpg" width="350px"><br>
  <i>⚠️This is my hobby project. I don't bother much about performance here</i>
</div>



<h2>✨Features</h2>
<h3>Download</h3>
<ul>
  <li>YouTube download (MP4/ MP3)</li>
  <li>Instagram download (Posts/Reals)</li>
  <li>TikTok download (in progress..)</li>
</ul>
<h3>Convert</h3>
<ul>
  <li>OGG to MP3</li>
  <li>M4A to MP3</li>
</ul>
<h3>Tools</h3>
<ul>
  <li>GPT 3.5 AI model</li>
  <li>Musical key finder🎵</li>
  <li>Weather forecast⛅️</li>
  <li>Air pollution level🏭</li>
  <li>Daily motivation in a form of videos🔋</li>
</ul>

<h2>⚙️Dependencies</h2>
<ul>
  <li>ffmpeg (to convert audio)</li>
  <li>Everything within requirements.txt</li>
</ul>

<h2>🌐Deploy</h2>
<ol>
    <li>Change the timezone of APScheduler depending on the location of your server <i>(bot.py)</i></li>
    <li>Add motivation search tags for <code>motive: list</code> env variable <i>(you can create .env file)</i></li>
    <li>Install the dependencies (Ubuntu example)</li>
    <ol>
        <li><code>sudo apt install ffmpeg</code></li>
        <li><code>source venv/bin/activate</code></li>
        <li><code>pip install -r requirements.txt</code></li>
    </ol>
    <li>Enjoy!</li>
</ol>
