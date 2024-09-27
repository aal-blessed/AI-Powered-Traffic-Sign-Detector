from flask import Flask, request, render_template
import torch
from torchvision import transforms
from PIL import Image
import io

app = Flask(__name__)

# Load the trained model 
model = torch.load('../models/model.pt')
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        img = Image.open(io.BytesIO(file.read()))
        img = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(img)
            prediction = torch.argmax(output, 1).item()
        label = 'Stop Sign' if prediction == 1 else 'Not a Stop Sign'
        return render_template('index.html', label=label)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
