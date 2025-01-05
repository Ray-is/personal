import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets
from torchvision import transforms

transform = transforms.ToTensor()
data = datasets.MNIST(root=r'.\data', train=True, download=True, transform=transform)
testdata = datasets.MNIST(root=r'.\data', train=False, download=True, transform=transform)
data_loader = DataLoader(data, batch_size=64, shuffle=True)
test_loader = DataLoader(testdata, batch_size=64, shuffle=False)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device: ", device)

class MNISTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 32)
        self.fc2 = nn.Linear(32, 10)
        self.activation = nn.ReLU()
        self.outputFunc = nn.Softmax(dim=1)

    def forward(self, x):
        hidden = self.activation(self.fc1(x))
        result = self.outputFunc(self.fc2(hidden))
        return result

def calculate_accuracy(loader, model, device):
    correct, total = 0, 0
    with torch.no_grad():
        for batchFeatures, batchLabels in loader:
            batchFeatures = batchFeatures.to(device).reshape(-1, 784)
            batchLabels = batchLabels.to(device)
            preds = model(batchFeatures).argmax(dim=1)
            correct += (preds == batchLabels).sum().item()
            total += batchLabels.size(0)
    return correct / total


num_epochs = 10
writer = SummaryWriter()
model = MNISTClassifier()
model = model.to(device)

sampleInput = torch.randn(1, 784).to(device)
writer.add_graph(model, sampleInput)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(num_epochs):
    print(epoch)
    testAccuracy = calculate_accuracy(test_loader, model, device)
    writer.add_scalar('Accuracy/test', testAccuracy, epoch)
    for name, param in model.named_parameters():
        writer.add_histogram(f'{name}_values', param, epoch)
        writer.add_histogram(f'{name}_gradients', 0 if param.grad is None else param.grad, epoch)

    for batchFeatures, batchLabels in data_loader:
        batchFeatures = batchFeatures.to(device).reshape(-1, 784)
        batchLabels = batchLabels.to(device)
        onehotLabels = torch.nn.functional.one_hot(batchLabels, 10)
        preds = model(batchFeatures)
        loss = criterion(preds, onehotLabels.float())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

writer.close()


