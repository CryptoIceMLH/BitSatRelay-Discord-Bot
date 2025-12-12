window.app = Vue.createApp({
  el: '#vue',
  mixins: [windowMixin],
  delimiters: ['${', '}'],
  data: function () {
    return {
      settings: {
        bot_token: '',
        enabled: false,
        rotation_speed: 30,
        lnbits_api_url: 'https://lnbits.molonlabe.holdings',
        announcements: ''
      }
    }
  },
  methods: {
    async getSettings() {
      try {
        const { data } = await LNbits.api.request(
          'GET',
          '/bitsatcredit_discord/api/v1/settings'
        )
        if (data) {
          // Convert announcements array to newline-separated string for textarea
          if (data.announcements && Array.isArray(data.announcements)) {
            data.announcements = data.announcements.join('\n')
          } else {
            data.announcements = ''
          }
          this.settings = data
        }
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    },
    async saveSettings() {
      try {
        // Convert announcements from textarea string to array
        const settingsToSave = { ...this.settings }
        if (typeof settingsToSave.announcements === 'string') {
          settingsToSave.announcements = settingsToSave.announcements
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
        }

        await LNbits.api.request(
          'POST',
          '/bitsatcredit_discord/api/v1/settings',
          null,
          settingsToSave
        )
        this.$q.notify({
          type: 'positive',
          message: 'Settings saved! Bot will update shortly.'
        })
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    }
  },
  created() {
    this.getSettings()
  }
})
