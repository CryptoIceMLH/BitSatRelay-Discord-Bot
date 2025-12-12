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
        lnbits_api_url: 'https://lnbits.molonlabe.holdings'
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
          this.settings = data
        }
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    },
    async saveSettings() {
      try {
        await LNbits.api.request(
          'POST',
          '/bitsatcredit_discord/api/v1/settings',
          null,
          this.settings
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
