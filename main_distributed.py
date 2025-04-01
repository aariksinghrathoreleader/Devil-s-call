import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from src.training.trainer import train_model

def main():
    dist.init_process_group("nccl")  # Initialize distributed training
    torch.cuda.set_device(0)  # Set device for the process

    train_model()  # Run training loop

if __name__ == "__main__":
    main()
