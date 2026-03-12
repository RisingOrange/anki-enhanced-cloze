from .ankiaddonconfig import ConfigManager, ConfigWindow

conf = ConfigManager()


def setup_config():
    conf.use_custom_window()
    conf.on_window_open(_on_config_window_open)
    conf.add_config_tab(_general_tab)


def _on_config_window_open(conf_window: ConfigWindow) -> None:
    """Ankiaddonconfig is used here in a non-standard way for configuring the note type options.
    The options don't really need to be saved in the config and they are overwritten with the values on the model when
    the config window is opened.
    """
    from .model import (
        config_values_from_model,
        add_or_update_model,
        update_model_options_with_config_values,
    )

    # Create the model if it doesn't exist
    add_or_update_model()

    # Load the config values from the model
    d = config_values_from_model()
    for key in d:
        conf.set(key, d[key])

    # Update the model when the config is saved
    conf_window.execute_on_save(update_model_options_with_config_values)


def _general_tab(conf_window: ConfigWindow) -> None:
    tab = conf_window.add_tab("General")

    tab.text("Shorcuts", bold=True)
    tab.shortcut_input(
        "revealNextGenuineClozeShortcut", "Shortcut to reveal next genuine cloze"
    )
    tab.shortcut_input(
        "revealAllGenuineClozesShortcut", "Shortcut to reveal all genuine clozes"
    )
    tab.shortcut_input(
        "revealNextPseudoClozeShortcut", "Shortcut to reveal next pseudo cloze"
    )
    tab.shortcut_input(
        "revealAllPseudoClozesShortcut", "Shortcut to reveal all pseudo clozes"
    )
    tab.hseparator()
    tab.space(8)

    tab.text("Border Actions", bold=True)
    tab.checkbox("swapLeftAndRightBorderActions", "Swap left and right border actions")
    tab.hseparator()
    tab.space(8)

    tab.text("Cloze Style", bold=True)
    tab.checkbox("underlineRevealedPseudoClozes", "Underline revealed pseudo clozes")
    tab.checkbox("underlineRevealedGenuineClozes", "Underline revealed genuine clozes")
    tab.hseparator()
    tab.space(8)

    tab.text("Cloze Behavior", bold=True)
    tab.checkbox("showHintsForPseudoClozes", "Show hints for pseudo clozes")
    tab.checkbox("revealPseudoClozesByDefault", "Reveal pseudo clozes by default")
    tab.hseparator()
    tab.space(8)

    tab.text("Auto Scroll to relevant cloze", bold=True)
    tab.checkbox("scrollToClozeOnToggle", "Scroll to cloze on toggle")
    tab.checkbox("animateScroll", "Animate scrolling")

    tab.stretch()
