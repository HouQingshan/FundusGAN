import warnings
import torch

# pylint: disable=redefined-builtin
# pylint: disable=arguments-differ
# pylint: disable=protected-access

#----------------------------------------------------------------------------

enabled = False  # Enable the custom op by setting this to true.

#----------------------------------------------------------------------------

def grid_sample(input, grid):
    if _should_use_custom_op():
        return _GridSample2dForward.apply(input, grid)
    return torch.nn.functional.grid_sample(input=input, grid=grid, mode='bilinear', padding_mode='zeros', align_corners=False)

#----------------------------------------------------------------------------

def _should_use_custom_op():
    if not enabled:
        return False
    if any(torch.__version__.startswith(x) for x in ['1.7.', '1.8.', '1.9']):
        return True
    warnings.warn(f'grid_sample_gradfix not supported on PyTorch {torch.__version__}. Falling back to torch.nn.functional.grid_sample().')
    return False

#----------------------------------------------------------------------------

class _GridSample2dForward(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, grid):
        assert input.ndim == 4
        assert grid.ndim == 4
        output = torch.nn.functional.grid_sample(input=input, grid=grid, mode='bilinear', padding_mode='zeros', align_corners=False)
        ctx.save_for_backward(input, grid)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, grid = ctx.saved_tensors
        grad_input, grad_grid = _GridSample2dBackward.apply(grad_output, input, grid)
        return grad_input, grad_grid

#----------------------------------------------------------------------------

class _GridSample2dBackward(torch.autograd.Function):
    @staticmethod
    def forward(ctx, grad_output, input, grid):
        op = torch._C._jit_get_operation('aten::grid_sampler_2d_backward')
        grad_input, grad_grid = op(grad_output, input, grid, 0, 0, False)
        ctx.save_for_backward(grid)
        return grad_input, grad_grid

    @staticmethod
    def backward(ctx, grad2_grad_input, grad2_grad_grid):
        _ = grad2_grad_grid # unused
        grid, = ctx.saved_tensors
        grad2_grad_output = None
        grad2_input = None
        grad2_grid = None

        if ctx.needs_input_grad[0]:
            grad2_grad_output = _GridSample2dForward.apply(grad2_grad_input, grid)

        assert not ctx.needs_input_grad[2]
        return grad2_grad_output, grad2_input, grad2_grid

#----------------------------------------------------------------------------
