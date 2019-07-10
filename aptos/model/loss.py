import torch
import torch.nn.functional as F

from .robust_loss_pytorch import AdaptiveLossFunction


def ce_loss(output, target):
    return F.cross_entropy(output, target)


def mse_loss(output, target):
    return F.mse_loss(output.squeeze(1), target.to(torch.float))


def l1_loss(output, target):
    return F.l1_loss(output.squeeze(1), target.to(torch.float))


class RobustLoss:

    def __init__(self, device, reduction='mean'):
        self.loss = AdaptiveLossFunction(num_dims=1, device=device, float_dtype=torch.float32)
        self.reduction = reduction

    def __call__(self, output, target):
        target = target.float().unsqueeze(1)
        if self.reduction == 'mean':
            return self.loss.lossfun(target - output).mean()
        if self.reduction == 'sum':
            return self.loss.lossfun(target - output).sum()
        raise

    def parameters(self):
        return self.loss.parameters()

    def named_parameters(self):
        return self.loss.named_parameters()
