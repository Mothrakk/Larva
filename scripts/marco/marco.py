import Larva

log_to_larva = lambda contents, use_timestamp=True: Larva.Log(contents, "marco", use_timestamp).to_larva(True)
log_to_larva("polo")
