import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'
import { Form, Formik } from 'formik'

import { Input } from '../components/Input'

storiesOf('components/Input', module).add('default', () => (
  <Formik
    initialValues={{ name: '' }}
    validate={() => ({ name: 'this is an error' })}
    onSubmit={({ name }) => {
      action('onSubmit')(name)
    }}
  >
    <Form>
      <Input label="Label name" name="name" placeholder="Please Enter..." />
    </Form>
  </Formik>
))
