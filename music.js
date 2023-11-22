const express = require('express');
const bodyParser = require('body-parser');
var player = require('play-sound')(opts = {})
const app = express();
app.use(bodyParser.json());
musicPlaying = false
app.post('/', async (req, res) => {
    const detectedEmotion = req.body.emotion;
    console.log('Received emotion:', detectedEmotion);
    if (detectedEmotion === 'happy') {
        if(musicPlaying === 'happy'){
            return;
        } 
        musicPlaying = 'happy'
        player.play('./music/happy.mp3', { afplay: ['-v', 1 ] /* lower volume for afplay on OSX */ }, function(err){
            if (err) throw err
          })
    }
    res.status(200).send('Emotion received');
});

app.listen(3000, () => {
    console.log('Express server running on port 3000');
});
