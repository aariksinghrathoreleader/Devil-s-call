import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from src.model.model import IJEPA
from src.data.dataset import get_dataloader

def train_model(epochs=10, lr=0.001, batch_size=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = IJEPA().to(device)
    
    dataloader = get_dataloader(batch_size=batch_size)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()  # Example loss function

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        
        for images, _ in tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}"):
            images = images.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, torch.zeros_like(outputs))  # Dummy target
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {epoch_loss / len(dataloader)}")

    torch.save(model.state_dict(), "checkpoint.pth")
    print("Training Complete. Model Saved.")

if __name__ == "__main__":
    train_model()
