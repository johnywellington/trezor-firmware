from trezor import res, ui, wire

from . import HomescreenBase


async def lockscreen() -> None:
    from apps.common.request_pin import can_lock_device
    from apps.base import unlock_device

    # Only show the lockscreen UI if the device can in fact be locked.
    if can_lock_device():
        await Lockscreen()
    # Otherwise proceed directly to unlock() call. If the device is already unlocked,
    # it should be a no-op storage-wise, but it resets the internal configuration
    # to an unlocked state.
    try:
        await unlock_device()
    except wire.PinCancelled:
        pass


class Lockscreen(HomescreenBase):
    BACKLIGHT_LEVEL = ui.BACKLIGHT_LOW

    def __init__(
        self, lock_label: str = "Locked", tap_label: str = "Tap to unlock"
    ) -> None:
        self.lock_label = lock_label
        self.tap_label = tap_label
        super().__init__()

    def render_lock(self) -> None:
        ui.display.bar_radius(40, 100, 160, 40, ui.TITLE_GREY, ui.BG, 4)
        ui.display.bar_radius(42, 102, 156, 36, ui.BG, ui.TITLE_GREY, 4)
        ui.display.text_center(
            ui.WIDTH // 2, 128, self.lock_label, ui.BOLD, ui.TITLE_GREY, ui.BG
        )

        ui.display.text_center(
            ui.WIDTH // 2 + 10, 220, self.tap_label, ui.BOLD, ui.TITLE_GREY, ui.BG
        )
        ui.display.icon(45, 202, res.load(ui.ICON_CLICK), ui.TITLE_GREY, ui.BG)

    def on_render(self) -> None:
        self.render_homescreen()
        self.render_lock()

    def on_touch_end(self, x: int, y: int) -> None:
        raise ui.Result(None)
