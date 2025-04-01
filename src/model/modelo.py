import torch
import torch.nn as nn
import torchvision.models as models

class IJEPA(nn.Module):
    def __init__(self, embed_dim=512):
        super(IJEPA, self).__init__()
        # Use Vision Transformer (ViT) as encoder
        self.encoder = models.vit_b_16(pretrained=True)  # Pretrained ViT model
        self.encoder.heads = nn.Identity()  # Remove classification head
        
        # Projection Head for Joint Embedding
        self.projection = nn.Sequential(
            nn.Linear(768, embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, embed_dim)
        )

    def forward(self, x):
        features = self.encoder(x)
        return self.projection(features)

# Example Usage
if __name__ == "__main__":
    model = IJEPA()
    dummy_input = torch.randn(2, 3, 224, 224)  # Batch of 2 images
    output = model(dummy_input)
    print(output.shape)  # Should be (2, 512)
