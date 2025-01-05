import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets
from torchvision import transforms
import matplotlib.pyplot as plt

transform = transforms.ToTensor()
data = datasets.MNIST(root=r'.\data', train=True, download=True, transform=transform)
testdata = datasets.MNIST(root=r'.\data', train=False, download=True, transform=transform)
data_loader = DataLoader(data, batch_size=64, shuffle=True)
test_loader = DataLoader(testdata, batch_size=64, shuffle=False)

train_and_overwrite = True

class AE(nn.Module):
    def __init__(self):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(784, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Linear(16, 2)
        )

        self.decoder = nn.Sequential(
            nn.Linear(2, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 784),
            nn.Sigmoid()
        )

    def forward(self, x):
        latent = self.encoder(x)
        decoded = self.decoder(latent)
        return decoded


def train(num_epochs=5):
    autoencoder.train()
    loss = 0
    criterion = nn.MSELoss()
    optimizer = optim.Adam(autoencoder.parameters(), lr=1e-3, weight_decay=1e-5)

    # Define Summary Writer
    writer = SummaryWriter('logs')

    for epoch in range(num_epochs):
        for batch, _ in data_loader:
            batch = batch.reshape(-1, 784)
            reconstruction = autoencoder(batch)
            loss = criterion(reconstruction, batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Write to Summary
        writer.add_scalar('Loss/train', loss, epoch)
        print(f"{epoch} | last loss: {loss:.5f}")

    autoencoder.eval()
    writer.close()


autoencoder = AE()

if train_and_overwrite:
    train()
    torch.save(autoencoder.state_dict(), r'.\saved_models\mnist_autoencoder.pt')
else:
    autoencoder.load_state_dict(torch.load(r'.\saved_models\mnist_autoencoder.pt'))
    autoencoder.eval()




""" 
~~~~ matplotlib visualization ~~~~

x_dist, y_dist = 1.5, 1.5  # x bounds = (-x_dist, x_dist) and y bounds = (-y_dist, y_dist). These both should be positive
def mouse_move(event):
    plt.clf()
    x, y = event.xdata, event.ydata
    x = 0 if x is None else (x/27) * 2 * x_dist - x_dist
    y = 0 if y is None else (y/27) * 2 * y_dist - y_dist
    print(x, y)

    with torch.no_grad():
        output = autoencoder.decoder(torch.Tensor((x, y)).unsqueeze(0))
    plt.imshow(output.reshape(28, 28), cmap='gray')
    plt.show()
plt.xlim(0, 27)
plt.ylim(27, 0)
plt.connect('motion_notify_event', mouse_move)
plt.show()
"""
