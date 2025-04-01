import torch
from src.model.model import IJEPA
from src.data.dataset import get_dataloader

def evaluate_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = IJEPA().to(device)
    model.load_state_dict(torch.load("checkpoint.pth"))  # Load trained model
    model.eval()

    dataloader = get_dataloader(batch_size=32)
    total_loss = 0.0
    
    with torch.no_grad():
        for images, _ in dataloader:
            images = images.to(device)
            outputs = model(images)
            total_loss += torch.mean(outputs).item()  # Example evaluation metric

    print(f"Evaluation Score: {total_loss / len(dataloader)}")

if __name__ == "__main__":
    evaluate_model()
