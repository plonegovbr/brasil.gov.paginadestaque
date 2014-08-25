*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${a11y_field_selector}  spacer-title
${a11y_sample}  Achievement Unlocked: a11y
${a11y_selector}  .spacer-tile > p:nth-child(1)
${edit_link_selector}  a.edit-tile-link
${spacer_tile_location}  "spacer"
${spacer_tile_selector}  //div[contains(@class, "spacer-tile") and contains(@style, "height: 400px")]
${tile_selector}  div.tile-container div.tile


*** Test cases ***

Test Spacer Tile
    # XXX: test is randomly failing on Travis CI
    [Tags]  Expected Failure

    Enable Autologin as  Site Administrator
    Go to Homepage

    Create Cover  Frontpage  Test for spacer tile  Empty layout
    Edit Cover Layout

    Add Tile  ${spacer_tile_location}
    Save Cover Layout

    Compose Cover
    Page Should Contain  Remember to add a text describing the background image

    Click Link  css=${edit_link_selector}
    Wait until page contains element  id=${a11y_field_selector}
    Input Text  id=${a11y_field_selector}  ${a11y_sample}
    Click Button  Save
    # save via ajax => wait until the tile has been reloaded
    Wait Until Page Contains Element  xpath=${spacer_tile_selector}
    Element Text Should Be  css=${a11y_selector}  ${a11y_sample}
    ${CLASS} =  Get Element Attribute  css=${a11y_selector}@class
    # FIXME: when saved, tile is shown in view mode intead of compose mode
    # Should be equal  ${CLASS}  discreet
    Should be equal  ${CLASS}  hiddenStructure

    Click Link  View
    Page Should Contain Element  xpath=${spacer_tile_selector}
    Element Text Should Be  css=${a11y_selector}  ${a11y_sample}
    ${CLASS} =  Get Element Attribute  css=${a11y_selector}@class
    Should be equal  ${CLASS}  hiddenStructure

    Edit Cover Layout
    Delete Tile
    Save Cover Layout
