from src.model.src_hifigan.model import MultiPeriodDiscriminator, MultiScaleDiscriminator
from src.model.src_mambavoc_v3.generator import Generator


from src.model.gan_base_model import GanBaseModel

import torch.nn as nn

class DiscriminatorModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.mpd = MultiPeriodDiscriminator()
        self.msd = MultiScaleDiscriminator()

    def forward(self, real_audio, generated_audio):
        # audio: [B, 1, T]
        y_df_hat_r_mpd, y_df_hat_g_mpd, fmap_f_r_mpd, fmap_f_g_mpd = self.mpd(real_audio, generated_audio)
        y_ds_hat_r_msd, y_ds_hat_g_msd, fmap_s_r_msd, fmap_s_g_msd = self.msd(real_audio, generated_audio)

        return {
            "MPD": {"y_df_hat_r": y_df_hat_r_mpd, "y_df_hat_g": y_df_hat_g_mpd, "fmap_f_r": fmap_f_r_mpd,
                    "fmap_f_g": fmap_f_g_mpd},
            "MSD": {"y_ds_hat_r": y_ds_hat_r_msd, "y_ds_hat_g": y_ds_hat_g_msd, "fmap_s_r": fmap_s_r_msd,
                    "fmap_s_g": fmap_s_g_msd},
        }

class MambaVocV3(GanBaseModel):
    def __init__(self, generator_params, inference_params=None):
        generator = Generator(**generator_params)
        discriminator = DiscriminatorModel()

        super().__init__(generator, discriminator)

        self.inference_params = inference_params

    def forward(self, **batch):
        x = batch["mel"]
        batch["pred_audio"] = self.generator(x, inference_params=self.inference_params)
        return batch
