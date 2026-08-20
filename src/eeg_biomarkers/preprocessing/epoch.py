def epoch_parameters(epoch_length_s: float, epoch_overlap_s: float) -> tuple[float, float]:
    """Return duration and step size for fixed-length epoching."""
    if epoch_overlap_s >= epoch_length_s:
        raise ValueError("epoch_overlap_s must be smaller than epoch_length_s")
    return epoch_length_s, epoch_length_s - epoch_overlap_s
